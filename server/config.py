import os

BASE_DIR = os.path.join(os.path.dirname(__file__), 'data')

DCMDIR = os.path.join(BASE_DIR, 'dcm')

DCMBAKDIR = os.path.join(BASE_DIR, 'dcm_bak')

NPYDIR = os.path.join(BASE_DIR, 'npy')

UPLOADDIR = os.path.join(BASE_DIR, 'upload')

UPLOADBAKDIR = os.path.join(BASE_DIR, 'upload_bak')

CHECKPOINTDIR = os.path.join(BASE_DIR, 'best.pth')