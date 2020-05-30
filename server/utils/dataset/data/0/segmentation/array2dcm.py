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
        output_path = self._out_dir / str(out_name)+'.dcm'
        self._writer.SetFileName(output_path)
        self._writer.Execute(image_slices)

    def get_series_tag(self, new_img, channels, patientid, patientname, pixel_dtype):
        modification_time = time.strftime('%H%M%S')
        modification_date = time.strftime('%Y%m%d')

        direction = new_img.GetDirection()
        series_tag_values = [("0008|0031",modification_time), # Series Time
                  ("0008|0021",modification_date), # Series Date
                  ("0008|0008","DERIVED\\SECONDARY"), # Image Type
                  ("0020|000e", "1.2.826.0.1.3680043.2.1125."+modification_date+".1"+modification_time), # Series Instance UID
                  ("0020|0037", '\\'.join(map(str, (direction[0], direction[3], direction[6],# Image Orientation (Patient)
                                                    direction[1],direction[4],direction[7])))),
                  ("0008|103e", "Created-SimpleITK")] # Series Description
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
                         ('0028|0008', '{}'.format(len(new_img))), #series number
                         ('0028|0002', str(channels)),
                         ("0008|0060", "CT"),# set the type to CT so the thickness is carried over
                         ("0020|0032", '\\'.join(map(str,new_img.TransformIndexToPhysicalPoint((0,0,i))))),# Image Position (Patient)
                         ("0020|0013", str(patientid)),
                        ]
        return series_tag_values

    def _kindey(self, img, predict):
        #提取肾
        predict = np.squeeze(predict)
        img = np.squeeze(img)
        segbin = np.greater(predict, 0)
        kindey = np.where(
            segbin,
            img,
            0
        )
        return kindey
    
    def _tumor(self, img, predict):
        predict = np.squeeze(predict)
        img = np.squeeze(img)
        segbin = np.greater(predict, 1)
        tumor = np.where(
            segbin,
            img,
            0
        )
        return tumor

    def _write_rgb(self, data):
        cmap = [[0, 0, 0], [0, 255, 0], [0, 0, 255]]
        cmap = np.array(cmap, dtype=np.int)

        img = data['image']
        img = np.squeeze(img)#channels, w, h)

        pred = data['predict']
        pred = np.squeeze(pred)
        preds = cmap[pred]
        preds = preds.transpose((0, 3, 1, 2))

        segbin = np.greater(pred, 0)
        segbin = np.stack([segbin]*3, 0)
        
        slices = np.where(
            segbin,
            np.round(0.3*preds+(1-alpha)*img).astype(np.uint8),
            np.round(img).astype(np.uint8)
        )

        pixel_dtype = 'float64'
        slices = np.array(slices, dtype=pixel_dtype)
        new_img = sitk.GetImageFromArray(slices)
        new_img.SetSpacing([0.9, 0.8, 0.7])
        self.writeSlices(self.get_series_tag(new_img, 3, data['index'], 'name_'+data['index']), new_img, data['index'])


    def _write_gray(self, data):
        img = data['image']
        predict = data['predict']
        kindey = self._kindey(img, predict)
        tumor = self._tumor(img, predict)
        slices = np.stack((img, kindey, tumor), 0)
        pixel_dtype = 'float64'
        slices = np.array(slices, dtype=pixel_dtype)
        new_img = sitk.GetImageFromArray(slices)
        new_img.SetSpacing([0.9, 0.8, 0.7])
        self.writeSlices(self.get_series_tag(new_img, 1, data['index'], 'name_'+data['index']), new_img, data['index'])

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
            if preds.shape[1] == self.num_classes:
                preds = preds.argmax(axis=1)
            preds = preds.transpose((0, 3, 1, 2))
            data['predict'] = preds
        
        if 'index' in data.keys() and data['index'] is not None:
            index = data['index']
            if type(index).__module__ != np.__name__:
                index = index.cpu().detach().numpy()
            data['index'] = index

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

    dc = DCMUtils('test')
    dc.rgb()
    print(dc.colortype)
    data = {}
    data['image'] = 
