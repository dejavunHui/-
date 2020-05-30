import cv2
import numpy as np
from albumentations import Compose

from albumentations import LongestMaxSize, PadIfNeeded


def to_numpy(data):

    image, label = data['image'], data['label']
    data['image'] = np.array(image)
    if data['label'] is not None:
        data['label'] = np.array(label)

    return data

class MedicalTransform:

    
    def __init__(self, output_size):

        if isinstance(output_size, (tuple, list)):
            self._output_size = output_size
        else:
            self._output_size = (output_size, output_size)

    def __call__(self, data):
        data = to_numpy(data)
        img, label = data['image'], data['label']
        is_3d = True if img.shape == 4 else False
        max_size = max(self._output_size[0], self._output_size[1])
        task = [
            LongestMaxSize(max_size, p=1),
            PadIfNeeded(self._output_size[0], self._output_size[1])
        ]

        aug = Compose(task)
        if not is_3d:
            aug_data = aug(image=img, mask=label)
            data['image'], data['label'] = aug_data['image'], aug_data['mask']

        else:
            keys = {}
            targets = {}
            for i in range(1, img.shape[2]):
                keys.update({f'image{i}': 'image'})
                keys.update({f'mask{i}': 'mask'})
                targets.update({f'image{i}': img[:, :, i]})
                targets.update({f'mask{i}': label[:, :, i]})
            aug.add_targets(keys)
            
            targets.update({'image': img[:, :, 0]})
            targets.update({'mask': label[:, :, 0]})
            
            aug_data = aug(**targets)
            imgs = [aug_data['image']]
            labels = [aug_data['mask']]
            
            for i in range(1, img.shape[2]):
                imgs.append(aug_data[f'image{i}'])
                labels.append(aug_data[f'mask{i}'])
            
            img = np.stack(imgs, axis=-1)
            label = np.stack(labels, axis=-1)
            data['image'] = img
            data['label'] = label
        
        return data
