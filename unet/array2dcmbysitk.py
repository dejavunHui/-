import SimpleITK as sitk
import time
from pathlib2 import Path
import numpy as np

pixel_dtypes = {"int16" : np.int16,
                "float64" : np.float64}


class DcmDataset:

    def __init__(self):
        pass

    def writeSlices(self, series_tag_values, new_img, out_dir, i):
        image_slice = new_img[:,:,i]
        image_slice = 

        # Tags shared by the series.
        list(map(lambda tag_value: image_slice.SetMetaData(tag_value[0], tag_value[1]), series_tag_values))

        # Slice specific tags.
        image_slice.SetMetaData("0008|0012", time.strftime("%Y%m%d")) # Instance Creation Date
        image_slice.SetMetaData("0008|0013", time.strftime("%H%M%S")) # Instance Creation Time
        image_slice.SetMetaData("0010|0020", '1'+str(i)) # patient id
        image_slice.SetMetaData("0010|0010", 'name'+str(i)) # patient name
        
        # Setting the type to CT preserves the slice location.
        image_slice.SetMetaData("0008|0060", "CT")  # set the type to CT so the thickness is carried over

        # (0020, 0032) image position patient determines the 3D spacing between slices.
        image_slice.SetMetaData("0020|0032", '\\'.join(map(str,new_img.TransformIndexToPhysicalPoint((0,0,i))))) # Image Position (Patient)
        image_slice.SetMetaData("0020|0013", str(i)) # Instance Number
        

        # Write to the output directory and add the extension dcm, to force writing in DICOM format.
        writer.SetFileName(os.path.join(out_dir, str(i)+'.dcm'))
        writer.Execute(image_slice)
        