from pathlib2 import Path
import cv2
import numpy as np
import nibabel as nib
from .kit import KitDataset
import pydicom

class Convertion:

    def __init__(self, output_dir, extentions=['*.jpg', '*.png', '*.nii.gz', '*.nii', '*.dcm']):

        self._extentions = extentions
        self._output_dir = Path(output_dir)
        if not self._output_dir.exists():
            self._output_dir.mkdir(parents=True)

    def get_files(self, root):
        """search all files in root path

        Arguments:
            root {[str or Path]} -- [文件根目录]
        """        
        root = Path(root)
        assert root.exists()
        files = []
        for extention in self._extentions:
            files += list(root.rglob(extention))
        return files
    
    def _convert(self, root):
       
        files = self.get_files(root)
        k = 0 if self._status == 'init' else len(list(self._output_dir.glob('*.npy')))
        for idx, file_ in enumerate(files):
            if '.jpg' in file_.parts[-1] or '.png' in file_.parts[-1]:
                img = cv2.imread(str(file_))
                cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img_arr = np.array(img)
                np.save(str(self._output_dir/'{:05}.npy'.format(k)), img_arr)
                k += 1
            elif '.nii.gz' in file_.parts[-1] or '.nii' in file_.parts[-1]:
                vol_nii =  nib.load(str(file_))
                vol = vol_nii.get_data()
                vol = KitDataset.normalize(vol, -512, 512)
                for i in range(vol.shape[0]):
                    np.save(str(self._output_dir/'{:05}.npy'.format(k)), vol[i])
                    k += 1
            elif '.dcm' in file_.parts[-1]:
                dc = pydicom.dcmread(str(file_))
                dc_array = dc.pixel_array
               
                if len(dc_array.shape) == 2:
                    np.save(str(self._output_dir/'{:05}.npy'.format(k)), dc_array)
                    k += 1
                else:
                    for i in range(dc_array.shape[0]):
                        np.save(str(self._output_dir/'{:05}.npy'.format(k)), dc_array[i])
                        k += 1
            print('success:{}/{}'.format(idx+1,len(files)))


    def __call__(self, root):
        self._convert(root)

    def is_add(self):
        self._status = 'add'
    
    def is_init(self):
        self._status = 'init'

    @property
    def status(self):
        return self._status


if __name__ == '__main__':
    convert = Convertion('test')
    convert.is_init()
    print(convert.status)
    convert('.')