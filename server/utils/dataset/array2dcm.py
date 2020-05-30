import SimpleITK as sitk
from pathlib2 import Path
import numpy as np
import cv2
import time
import datetime


class DCMUtils:

    def __init__(self, out_dir):
        self._pixel_dtypes = {
            'int16': np.int16,
            'float64': np.float64
        }
        self._writer = sitk.ImageFileWriter()
        self._writer.KeepOriginalImageUIDOn()
        self._out_dir = Path(out_dir)
        self._rgb = False
        
    def writeSlices(self, series_tag_values, new_img, out_name):
        '''
        写入帧序列,目前尚未完成rgb帧写入
        '''
        image_slices = new_img
        list(map(lambda tag_value: image_slices.SetMetaData(tag_value[0], tag_value[1]), series_tag_values))
        
        if not self._out_dir.exists():
            self._out_dir.mkdir(parents=True)
        output_path = self._out_dir / '{}.dcm'.format(out_name)
        self._writer.SetFileName(str(output_path))
        self._writer.Execute(image_slices)

    def get_series_tag(self, new_img, channels, patientid, patientname, pixel_dtype):
        modification_time = time.strftime('%H%M%S')
        modification_date = time.strftime('%Y%m%d')

        direction = new_img.GetDirection()
        series_tag_values = [("0008|0031",modification_time), # Series Time
                  ("0008|0021",modification_date), # Series Date
                  ("0008|0008","DERIVED\\SECONDARY"), # Image Type
                  ("0020|000e", "1.2.826.0.1.3680043.2.1125."+modification_date+".1"+modification_time), # Series Instance UID
                  
                  ("0008|103e", "Created-SimpleITK")] # Series Description
        if channels == 1:
            series_tag_values = series_tag_values + \
                [("0020|0037", '\\'.join(map(str, (direction[0], direction[3], direction[6],# Image Orientation (Patient)
                                                    direction[1],direction[4],direction[7]))))]
        else:
            series_tag_values = series_tag_values + \
                [("0020|0037", '\\'.join(map(str, (direction[0], direction[3],# Image Orientation (Patient)
                                                    direction[1]))))]
        if self._pixel_dtypes[pixel_dtype] == np.float64:
            rescale_slope = 0.001 #keep three digits after the decimal point
            series_tag_values = series_tag_values + \
                        [('0028|1053', str(rescale_slope)), #rescale slope
                         ('0028|1052','0'),   #rescale intercept
                         ('0028|0100', '16'), #bits allocated
                         ('0028|0101', '16'), #bits stored
                         ('0028|0102', '15'), #high bit
                         ('0028|0103','0')] #pixel representation
        series_tag_values = series_tag_values + \
                        [('0008|0012', time.strftime("%Y%m%d")), # Instance Creation Date
                         ('0008|0013', time.strftime("%H%M%S")),# Instance Creation Time
                         ("0010|0020", str(patientid)), #patient id
                         ("0010|0010", str(patientname)), #patient name
                         ('0020|0011', '{}'.format(new_img.GetDepth()//channels)), #series number
                         ('0020|0013', '{}'.format(new_img.GetDepth()//channels)), #image number
                         ('0028|0008', '{}'.format(new_img.GetDepth()//channels)), #numbers of frame
                         ('0028|0002', str(channels)),
                         ("0008|0060", "CT"),# set the type to CT so the thickness is carried over
                         ("0020|0032", '\\'.join(map(str,new_img.TransformIndexToPhysicalPoint((0,0,0))))),# Image Position (Patient)
                         ("0020|0013", str(patientid)),
                        ]
        return series_tag_values

    def _kindey(self, img, predict):
        #提取肾
        predict = np.squeeze(predict)
        img = np.squeeze(img)
        if len(img.shape) == 3:
            img = img[0]
        segbin = np.greater(predict, 0)
        kindey = np.where(
            segbin,
            img,
            0.001
        )
        return kindey
    
    def _tumor(self, img, predict):
        predict = np.squeeze(predict)
        img = np.squeeze(img)
        if len(img.shape) == 3:
            img = img[0]
        segbin = np.greater(predict, 1)
        tumor = np.where(
            segbin,
            img,
            0.001
        )
        return tumor

    def _write_rgb(self, data):
        cmap = [[0, 0, 0], [0, 255, 0], [0, 0, 255]]
        cmap = np.array(cmap, dtype=np.int)

        imgs = data['image']
        predss = data['predict']

        for i in range(len(img)):
            img = np.squeeze(imgs[i])#channels, w, h)
            pred = np.squeeze(predss[i])
            preds = cmap[pred]
            preds = preds.transpose((2, 0, 1))

            segbin = np.greater(pred, 0)
            segbin = np.stack([segbin]*3, 0)
            
            slices = np.where(
                segbin,
                np.round(0.3*preds+(1-0.3)*img).astype(np.uint8),
                np.round(img).astype(np.uint8)
            )
            pixel_dtype = 'float64'
            slices = np.array(slices, dtype=pixel_dtype)
            new_img = sitk.GetImageFromArray(slices, sitk.sitkVectorUInt8)
            new_img.SetSpacing([0.9, 0.8, 0.7])
            series = self.get_series_tag(new_img, 3, data['index'], 'name_{}_{}_{}'.format(data['index'], data['name'][0], i), 'float64')
            self.writeSlices(series, new_img, '{}_{}_{}'.format(data['name'][0], data['index'], i))


    def _write_gray(self, data):
        img = data['image']
        predict = data['predict']
        for i in range(img.shape[0]):
            kindey = self._kindey(img[i,0], predict[i])
            tumor = self._tumor(img[i,0], predict[i])
            print(kindey.shape, img.shape, tumor.shape)
            slices = np.stack((img[i,0], kindey, tumor), 0)
            pixel_dtype = 'float64'
            slices = np.array(slices, dtype=pixel_dtype)
            new_img = sitk.GetImageFromArray(slices)
            new_img.SetSpacing([0.9, 0.8, 0.7])
            self.writeSlices(self.get_series_tag(new_img, 1, data['index'], 'name_{}_{}_{}'.format(data['index'], data['name'][0], i), 'float64'), new_img, '{}_{}_{}'.format(data['name'][0], data['index'],i))

    def __call__(self, data):
        if 'image' in data.keys() and data['image'] is not None:
            imgs = data['image']
            if type(imgs).__module__ != np.__name__:
                imgs = imgs.cpu().detach().numpy()
            data['image'] = imgs
        
        if 'predict' in data.keys() and data['predict'] is not None:
            preds = data['predict']
            if type(preds).__module__ != np.__name__:
                preds = preds.cpu().detach().numpy()
            if preds.shape[1] == 3:
                preds = preds.argmax(axis=1)
            data['predict'] = preds
        
        if 'index' in data.keys() and data['index'] is not None:
            index = data['index']
            if type(index).__module__ != np.__name__:
                index = index.cpu().detach().numpy()
            data['index'] = index[0]

        print(data['name'],type(data['name']))
        if not self._rgb:
            self._write_gray(data)
        else:
            self._write_rgb(data)


    def rgb(self):
        self._rgb = True

    def gray(self):
        self._rgb = False

    @property
    def colortype(self):
        return 'rgb' if self._rgb else 'gray'


if __name__ == '__main__':
    import torch
    dc = DCMUtils('test')
    # dc.rgb()#rgb暂时不能正常工作
    dc.gray()
    print(dc.colortype)
    data = {}
    data['image'] = np.load('./data/0/imaging/047.npy')
    data['predict'] = np.load('./data/0/segmentation/047.npy')
    # print(data['image'].shape,data['predict'].shape)
    data['index'] = torch.Tensor(3)
    dc(data)
