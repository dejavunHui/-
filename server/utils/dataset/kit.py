import torch.nn as nn
import torch
from torch.utils import data
from pathlib2 import Path
from albumentations import Compose, PadIfNeeded, Resize
import cv2
import nibabel as nib
import numpy as np
from .transform import to_numpy


class KitDataset(data.Dataset):

    """数据集
    """        
    def __init__(self, root, stack_num=3, img_size=(512, 512), transform=None):
        
        self._root = Path(root)
        self._stack_num = stack_num

        self._img_size = img_size if isinstance(img_size, (list, tuple)) else (img_size, img_size)
        self._transform = transform
        self._get_data()
        self._img_channels = self.__getitem__(0)['image'].shape[0]

    def _get_data(self):
        
        self._imgs = list(self._root.glob('*.npy'))
        self._imgs.sort()

    def get_stack_num(self, idx):

        data_path = self._imgs[idx]
        img = np.load(str(data_path))
        imgs = [img] * self._stack_num
        imgs = np.stack(imgs, axis=2)
        data = {'image': imgs, 'label': None, 'index': idx, 'name': data_path.name.split('.')[0]}

        return data

    def __getitem__(self, idx):

        data = self.get_stack_num(idx)
        data = self._transform(data)
        data = self._default_transform(data)

        return data
        
    def __len__(self):
        return len(self._imgs)

    @staticmethod
    def normalize(volume, hu_min, hu_max):
        if hu_min is not None or hu_max is not None:
            volume = np.clip(volume,hu_min,hu_max)

        mxval = np.max(volume)
        mnval = np.min(volume)
        im_volume = (volume - mnval)/max(mxval - mnval, 1e-3)
        return im_volume
        
    def _resize(self, data):
        data = to_numpy(data)
        img, label = data['image'], data['label']
        num = max(img.shape[0], img.shape[1])

        aug = Compose([
            PadIfNeeded(min_height=num, min_width=num, border_mode=cv2.BORDER_CONSTANT, p=1),
            Resize(height=self._img_size[0], width=self._img_size[1], p=1)
        ])

        data = aug(img=img, mask=label)
        img, label = data['image'], data['mask']

        data['image'] = img
        data['label'] = label
        return data
                
    def _default_transform(self, data):
        if (data['image'].shape[0], data['image'].shape[1]) != self._img_size:
            data = self._resize(data)
        
        image, label = data['image'], data['label']
        
        image = image.astype(np.float32)
        image = image.transpose((2, 0, 1))
        image = torch.from_numpy(image)
        data['image'] = image
        data['label'] = torch.Tensor()
        
        return data

    def vis_transform(slef, data):
        cmap = [[0, 0, 0], [0, 255, 0], [0, 0, 255]]
        cmap = np.array(cmap, dtype=np.int)
        if 'image' in data.keys() and data['image'] is not None:
            imgs = data['image']
            if type(imgs).__module__ != np.__name__:
                imgs = imgs.cpu().detach().numpy()
            data['image'] = imgs
        
        if 'label' in data.keys() and data['label'] is not None and data['label'].shape[-1] != 0:
            labels = data['label']
            if type(labels).__module__ != np.__name__:
                labels = labels.cpu().detach().numpy()
            labels = cmap[labels]
            labels = labels.transpose((0, 3, 1, 2))
            labels = labels / 255
            data['label'] = labels
        
        if 'predict' in data.keys() and data['predict'] is not None:
            preds = data['predict']
            if type(preds).__module__ != np.__name__:
                preds = preds.cpu().detach().numpy()
            if preds.shape[1] == self.num_classes:
                preds = preds.argmax(axis=1)
            preds = cmap[preds]
            preds = preds.transpose((0, 3, 1, 2))
            preds = preds / 255
            data['predict'] = preds
        return data
    
    @property
    def img_channels(self):
        return self._img_channels

    @property
    def stack_num(self):
        return self._stack_num