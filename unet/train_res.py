import sys

import click
import numpy as np
import torch
import torch.nn as nn
from pathlib2 import Path

from tensorboardX import SummaryWriter
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler
from tqdm import tqdm

import utils.checkpoint as cp
from dataset import kitdataset
from dataset.transform import MedicalTransform
from net.resunet import ResUNet
from utils.visualize import imshow
from utils.metrics import Evaluator

from torch.autograd import Variable

@click.command()
@click.option('-e', '--epoch', 'epoch_num', help='Number of training epoch', type=int, default=500, show_default=True)
@click.option('-b', '--batch', 'batch_size', help='Number of batch size', type=int, default=16, show_default=True)
@click.option('-l', '--lr', help='Learning rate', type=float, default=0.0001, show_default=True)
@click.option('-g', '--num_gpu', help='Number of GPU', type=int, default=1, show_default=True)
@click.option('-s', '--size', 'img_size', help='Output image size', type=(int, int),
              default=(512, 512), show_default=True)
@click.option('-d', '--data', 'data_path', help='Path of kits19 data after conversion',
              type=click.Path(exists=True, dir_okay=True, resolve_path=True),
              default='datanpy', show_default=True)
@click.option('--log', 'log_path', help='Checkpoint and log file save path',
              type=click.Path(dir_okay=True, resolve_path=True),
              default='log', show_default=True)
@click.option('-r', '--resume', help='Resume checkpoint file to continue training',
              type=click.Path(exists=True, file_okay=True, resolve_path=True), default=None)
@click.option('--eval_intvl', help='Number of epoch interval of evaluation. '
                                   'No evaluation when set to 0',
              type=int, default=1, show_default=True)
@click.option('--cp_intvl', help='Number of epoch interval of checkpoint save. '
                                 'No checkpoint save when set to 0',
              type=int, default=1, show_default=True)
@click.option('--vis_intvl', help='Number of iteration interval of display visualize image. '
                                  'No display when set to 0',
              type=int, default=0, show_default=True)
@click.option('--num_workers', help='Number of workers on dataloader. '
                                    'Recommend 0 in Windows. '
                                    'Recommend num_gpu in Linux',
              type=int, default=1, show_default=True)
def main(epoch_num, batch_size, lr, num_gpu, img_size, data_path, log_path,
         resume, eval_intvl, cp_intvl, vis_intvl, num_workers):
    data_path = Path(data_path)
    log_path = Path(log_path)
    cp_path = log_path / 'checkpoint'

    #使用上次训练的文件继续训练
    if not resume and log_path.exists() and len(list(log_path.glob('*'))) > 0:
        print(f'log path "{str(log_path)}" has old file', file=sys.stderr)
        sys.exit(-1)
    
    if not cp_path.exists():
        cp_path.mkdir(parents=True)

    transform = MedicalTransform(output_size=img_size, roi_error_range=15, use_roi=False)
    dataset = kitdataset.KitDataSet(data_path, stack_num=5, spec_classes=[0, 1, 1], img_size=img_size,
                                    use_roi=False, train_transform=transform, valid_transform=transform)               

    net = ResUNet(in_ch=dataset.img_channels, out_ch=dataset.num_classes, base_ch=64)
    optimizer = torch.optim.Adam(net.parameters(), lr=lr)

    start_epoch = 0
    #如果之前训练的参数存在，则进行加载
    if resume:
        data = {
            'net': net,
            'optimizer': optimizer,
            'epoch': 0
        }
        cp_file = Path(resume)
        cp.load_params(data, cp_file, device='cpu')
        start_epoch = data['epoch'] + 1

    criterion = nn.CrossEntropyLoss()

    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.1, patience=5, verbose=True,
        threshold=0.0001, threshold_mode='rel', cooldown=0, min_lr=0, eps=1e-08
    )

    logger = SummaryWriter(str(log_path))

    gpu_ids = [i for i in range(num_gpu)]

    print(f'{" Start training ":-^40s}\n')
    msg = f'Net: {net.__class__.__name__}\n' + \
          f'Dataset: {dataset.__class__.__name__}\n' + \
          f'Epochs: {epoch_num}\n' + \
          f'Learning rate: {optimizer.param_groups[0]["lr"]}\n' + \
          f'Batch size: {batch_size}\n' + \
          f'Device: cuda{str(gpu_ids)}\n'
    print(msg)

    torch.cuda.empty_cache()

    #在gpu上训练
    net = torch.nn.DataParallel(net, device_ids=gpu_ids).cuda()
    # net = torch.nn.DataParallel(net, device_ids=gpu_ids).cpu()

    criterion = criterion.cuda()
    # for state in optimizer.cuda():
    #     for k, v in state.items():
    #         if isinstance(v, torch.Tensor):
    #             state[k] = v.cuda()

    # criterion = criterion.cpu()
    # for state in optimizer.cuda():
    #     for k, v in state.items():
    #         if isinstance(v, torch.Tensor):
    #             state[k] = v.cpu()

    
    vaild_score = 0.0
    best_score = 0.0
    best_epoch = 0.0

    for epoch in range(start_epoch, epoch_num):
        epoch_str = f'Epoch {epoch+1}/{epoch_num}'
        print(f'{epoch_str:-^40s}')
        print(f'Learning rate: {optimizer.param_groups[0]["lr"]}')

        net.train()
        torch.set_grad_enabled(True)
        transform.train()
        try:
            loss = training(net, dataset, criterion, optimizer, scheduler,
                            epoch, batch_size, num_workers, vis_intvl, logger)
            
            if eval_intvl > 0 and (epoch + 1) % eval_intvl == 0:
                net.eval()
                torch.set_grad_enabled(False)
                transform.eval()
                
                train_score = evaluation(net, dataset, epoch, batch_size, num_workers, vis_intvl, logger, type='train')
                vaild_score = evaluation(net, dataset, epoch, batch_size, num_workers, vis_intvl, logger, type='valid')
                
                print(f'Train data score: {train_score:.5f}')
                print(f'Valid data score: {vaild_score:.5f}')
            
            if vaild_score > best_score:
                best_score = vaild_score
                best_epoch = epoch
                cp_file = cp_path / 'best.pth'
                cp.save(epoch, net.module, optimizer, str(cp_file))
                print('Update best acc!')
                logger.add_scalar('best/epoch', best_epoch + 1, 0)
                logger.add_scalar('best/score', best_score, 0)
            
            if (epoch + 1) % cp_intvl == 0:
                cp_file = cp_path / f'cp_{epoch + 1:03d}.pth'
                cp.save(epoch, net.module, optimizer, str(cp_file))
            
            print(f'Best epoch: {best_epoch + 1}')
            print(f'Best score: {best_score:.5f}')
        
        except KeyboardInterrupt:
            cp_file = cp_path / 'INTERRUPTED.pth'
            cp.save(epoch, net.module, optimizer, str(cp_file))
            return


def training(net, dataset, criterion, optimizer, scheduler, epoch, base_size, num_workers, vis_intvl, logger):

    sampler = RandomSampler(dataset.train_dataset)
    train_loader = DataLoader(dataset.train_dataset, batch_size=base_size, sampler=sampler,
                    num_workers=num_workers, pin_memory=True)
    
    tbar = tqdm(train_loader, ascii=True, desc='train', dynamic_ncols=True)
    for batch_idx, data in enumerate(tbar):
        #训练过程
        imgs, labels = data['image'].cuda(), data['label'].cuda()
        # imgs, labels = data['image'].cpu(), data['label'].cpu()
        outputs = net(imgs)
        loss = criterion(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if vis_intvl > 0 and batch_idx % vis_intvl == 0:
            data['predict'] = outputs
            data = dataset.vis_transform(data)
            imgs, labels, predicts = data['image'], data['label'], data['predict']
            imshow(title='Train', imgs=(imgs[0, dataset.img_channels // 2], labels[0], predicts[0]),
                    shape=(1,3), subtitle=('image','label','predict'))
        
        tbar.set_postfix(loss=f'{loss.item():.5f}')

    scheduler.step(loss.item())

    logger.add_scalar('loss', loss.item(), epoch)
    return loss.item()


def evaluation(net, dataset, epoch, batch_size, num_workers, vis_intvl, logger, type):
    type = type.lower()
    if type == 'train':
        subset = dataset.train_dataset
        case_slice_indices = dataset.train_case_slice_indices
    elif type == 'valid':
        subset = dataset.valid_dataset
        case_slice_indices = dataset.valid_case_slice_indices
    
    sampler = SequentialSampler(subset)
    data_loader = DataLoader(subset, batch_size=batch_size, sampler=sampler,
                             num_workers=num_workers, pin_memory=True)
    evaluator = Evaluator(dataset.num_classes)
    
    case = 0
    vol_label = []
    vol_output = []
    
    with tqdm(total=len(case_slice_indices) - 1, ascii=True, desc=f'eval/{type:5}', dynamic_ncols=True) as pbar:
        for batch_idx, data in enumerate(data_loader):
            imgs, labels, idx = data['image'].cuda(), data['label'], data['index']
            # imgs, labels, idx = data['image'].cpu(), data['label'], data['index']
            
            outputs = net(imgs)
            outputs = outputs.argmax(dim=1)
            
            labels = labels.cpu().detach().numpy()
            outputs = outputs.cpu().detach().numpy()
            idx = idx.numpy()
            
            vol_label.append(labels)
            vol_output.append(outputs)
            
            while case < len(case_slice_indices) - 1 and idx[-1] >= case_slice_indices[case + 1] - 1:
                vol_output = np.concatenate(vol_output, axis=0)
                vol_label = np.concatenate(vol_label, axis=0)
                
                vol_num_slice = case_slice_indices[case + 1] - case_slice_indices[case]
                evaluator.add(vol_output[:vol_num_slice], vol_label[:vol_num_slice])
                
                vol_output = [vol_output[vol_num_slice:]]
                vol_label = [vol_label[vol_num_slice:]]
                case += 1
                pbar.update(1)
            
            if vis_intvl > 0 and batch_idx % vis_intvl == 0:
                data['predict'] = outputs
                data = dataset.vis_transform(data)
                imgs, labels, predicts = data['image'], data['label'], data['predict']
                imshow(title=f'eval/{type:5}', imgs=(imgs[0, dataset.img_channels // 2], labels[0], predicts[0]),
                       shape=(1, 3), subtitle=('image', 'label', 'predict'))
    
    acc = evaluator.eval()
    
    for k in sorted(list(acc.keys())):
        if k == 'dc_each_case': continue
        print(f'{type}/{k}: {acc[k]:.5f}')
        logger.add_scalar(f'{type}_acc_total/{k}', acc[k], epoch)
    
    for case_idx in range(len(acc['dc_each_case'])):
        case_id = dataset.case_idx_to_case_id(case_idx, type)
        dc_each_case = acc['dc_each_case'][case_idx]
        for cls in range(len(dc_each_case)):
            dc = dc_each_case[cls]
            logger.add_scalar(f'{type}_acc_each_case/case_{case_id:05d}/dc_{cls}', dc, epoch)
    
    score = acc['dc_per_case_1']
    logger.add_scalar(f'{type}/score', score, epoch)
    return score



if __name__ == '__main__':
    main()