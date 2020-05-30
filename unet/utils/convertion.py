from niiutils import load_case,ROOT_PATH
import numpy as np
import os
import glob

def normalize(volume,hu_min,hu_max):
    if hu_min is not None or hu_max is not None:
        volume = np.clip(volume,hu_min,hu_max)

    mxval = np.max(volume)
    mnval = np.min(volume)
    im_volume = (volume - mnval)/max(mxval - mnval, 1e-3)
    return im_volume


def conversion(cid,npypath):
    vol_nii,seg_nii = load_case(cid)
    vol = vol_nii.get_data()
    vol = normalize(vol,-512,512)
    npy_root = os.path.join(ROOT_PATH,npypath,str(cid))#新建npy数据存放目录
    if not os.path.exists(npy_root):
        os.makedirs(npy_root)

    vol_npy_path = os.path.join(npy_root,'imaging')
    if not os.path.exists(vol_npy_path):
        os.mkdir(vol_npy_path)
    if len(list(glob.glob(os.path.join(vol_npy_path,'*.npy')))) != vol.shape[0]:
        for i in range(vol.shape[0]):
            np.save(os.path.join(vol_npy_path,'{:03}.npy'.format(i)),vol[i])
    #存储seg
    seg = seg_nii.get_data()
    seg_npy_path = os.path.join(npy_root,'segmentation')
    if not os.path.exists(seg_npy_path):
        os.mkdir(seg_npy_path)
    if len(list(glob.glob(os.path.join(seg_npy_path,'*.npy'))))!=seg.shape[0]:
        for i in range(seg.shape[0]):
            np.save(os.path.join(seg_npy_path,'{:03}.npy'.format(i)),seg[i])

    affine_npy_path = npy_root
    affine = vol_nii.affine
    np.save(os.path.join(affine_npy_path,'affine.npy'),affine)
    print('{} transform success!'.format(cid))


def conversion_all():
    for i in range(16):
        conversion(str(i),'datanpy')


if __name__ == '__main__':
    conversion_all()