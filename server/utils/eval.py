import torch.nn as nn
import numpy as np
import torch
from pathlib2 import Path
from .denseunet import DenseUNet
from .dataset.kit import KitDataset
from .dataset.transform import MedicalTransform
from .checkpoint import load_params
from torch.utils.data import DataLoader, SequentialSampler

class Eval:

    def __init__(self, bach_size, img_size, data_path, resume):
        self._batch_size = bach_size
        self._img_size = img_size
        self._data_path = Path(data_path)
        self._resume = Path(resume)
        self._dataset = KitDataset(data_path, stack_num=3, img_size=img_size, transform=MedicalTransform(img_size))
        self._net = DenseUNet(in_ch=self._dataset.stack_num, out_ch=self._dataset.img_channels)
        self._sampler = SequentialSampler(self._dataset)
        self._data_loader = DataLoader(self._dataset, batch_size=self._batch_size, sampler=self._sampler, num_workers=1, pin_memory=True)
        self.load_params()

    def load_params(self):

        assert self._resume.exists()
        data = {'net': self.net}
        load_params(data, self._resume)
        print(f'{" Start evaluation ":-^40s}\n')
        msg = f'Net: {self._net.__class__.__name__}\n' + \
            f'Batch size: {self._batch_size}\n'
        print(msg)
        self._net.eval()
        torch.set_grad_enabled(False)
    
        
    def __call__(self):
        for batch_idx, data in enumerate(self._data_loader):
            imgs = data['image'].cpu()
            outputs = self._net(imgs)
            predicts = outputs['output']
            predicts = predicts.argmax(dim=1)
            predicts = predicts.cpu().detach().numpy()
            data['predict'] = predicts
            yield data

    @property
    def dataset(self):
        return self._dataset

    @property
    def img_size(self):
        return self._img_size

    @property
    def net(self):
        return self._net

if __name__ == '__main__':
    e = Eval(3, 512, './dataset/data/0/imaging/', './best.pth')
    for data in e():
        print(data['predict'].shape)