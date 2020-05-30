'''
将dcm结果上传到dcm4chee服务器
'''

import subprocess
from .dataset.array2dcm import DCMUtils
from pathlib2 import Path
import os, shutil

def upload(dcm_path, dcm_back_path):
    server = 'storescu -c DCM4CHEE@localhost:104 {}'
    dcm = Path(dcm_path)
    dcm_back = Path(dcm_back_path)
    assert dcm.exists()
    if not dcm_back.exists():
        dcm_back.mkdir(parents=True)
    
    files = dcm.glob('*.dcm')
    for file_ in files:
        server_ = server.format(str(file_))
        returncode = subprocess.call(server_, shell=True)
        if returncode == 0:
            shutil.move(str(file_), str(dcm_back))
            
        
        
if __name__ == '__main__':
    upload('./dataset/test', './test_back')