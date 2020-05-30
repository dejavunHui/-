import numpy as np
import os
from imageio import imwrite
from utils.niiutils import load_case,ROOT_PATH
from matplotlib import pyplot as plt
import scipy.misc
import argparse

DEFAULT_KIDNEY_COLOR = [255,0,0]
DEFAULT_TUMOR_COLOR = [0,0,255]
DEFAULT_HU_MAX = 512
DEFAULT_HU_MIN = -512
DEFAULT_OVERLAY_ALPHA = 0.3
DEFAULT_PLANE = 'axial'

def hu_to_grayscale(volume,hu_min,hu_max):

    '''
    图像灰度化
    '''

    if hu_min is not None or hu_max is not None:
        volume = np.clip(volume,hu_min,hu_max)

    mxval = np.max(volume)
    mnval = np.min(volume)
    im_volume = (volume - mnval)/max(mxval - mnval, 1e-3)


    im_volume = 255*im_volume
    return np.stack((im_volume,im_volume,im_volume),axis=-1)

def class_to_color(segmentation,k_color,t_color):
    
    shp = segmentation.shape
    seg_color = np.zeros((shp[0],shp[1],shp[2],3),dtype=np.float32)

    seg_color[np.equal(segmentation,1)] = k_color
    seg_color[np.equal(segmentation,2)] = t_color
    return seg_color


def overlay(volume_ims, segmentation_ims, segmentation,alpha):

    segbin = np.greater(segmentation, 0)#产生bool数组
    repeated_segbin = np.stack((segbin,segbin,segbin),axis=-1)


    overlayed = np.where(
        repeated_segbin,
        np.round(alpha*segmentation_ims+(1-alpha)*volume_ims).astype(np.uint8),
        np.round(volume_ims).astype(np.uint8)
    )
    return overlayed

def display(cid, destionation=None,hu_min=DEFAULT_HU_MIN,hu_max=DEFAULT_HU_MAX,
    k_color = DEFAULT_KIDNEY_COLOR,
    t_color = DEFAULT_TUMOR_COLOR,
    alpha = DEFAULT_OVERLAY_ALPHA,
    plane=DEFAULT_PLANE):
    
    plane = plane.lower()
    
    plane_opts = ['axial', 'coronal', 'sagittal']#轴向、冠状、矢状显示
    if plane not in plane_opts:
        raise ValueError((
        'Plane \"{}\" not understood.Must be one of following\n\n\t{}\n'
        ).format(plane_opts,plane_opts)
    )
    out_path = None
    if destionation:
        out_path = destionation
    if out_path and not os.path.exists(out_path):
        os.mkdir(out_path)
    #加载case数据
    vol,seg = load_case(cid)
    spacing = vol.affine
    vol = vol.get_data()
    seg = seg.get_data()
    seg = seg.astype(np.int32)
    #转换可显示的格式
    vol_ims = hu_to_grayscale(vol,hu_min,hu_max)
    seg_ims = class_to_color(seg,k_color,t_color)

    if plane == plane_opts[0]:#轴状显示

        viz_ims = overlay(vol_ims,seg_ims,seg,alpha)
        if out_path:
            for i in range(np.shape(viz_ims)[0]):
                fpath = os.path.join(out_path,'{:05d}.png'.format(i))
                imwrite(fpath,viz_ims[i])
    
    if plane == plane_opts[1]:
        spc_ratio = np.abs(np.sum(spacing[2,:]))/np.abs(np.sum(spacing[0,:]))
        ims = []
        for i in range(np.shape(vol_ims)[1]):
            vol_im = scipy.misc.imresize(
                vol_ims[:,i,:], (
                    int(vol_ims.shape[0]*spc_ratio),
                    int(vol_ims.shape[2])
                ), interp="bicubic"
            )
            seg_im = scipy.misc.imresize(
                seg_ims[:,i,:], (
                    int(vol_ims.shape[0]*spc_ratio),
                    int(vol_ims.shape[2])
                ), interp="nearest"
            )
            sim = scipy.misc.imresize(
                seg[:,i,:], (
                    int(vol_ims.shape[0]*spc_ratio),
                    int(vol_ims.shape[2])
                ), interp="nearest"
            )
            viz_im = overlay(vol_im, seg_im, sim, alpha)
            ims.append(viz_im)
            if out_path:
                fpath = os.path.join(out_path,'{:05d}.png'.format(i))
                imwrite(fpath,viz_im)
        viz_ims = np.stack(ims)

    if plane == plane_opts[2]:
        spc_ratio = np.abs(np.sum(spacing[2,:]))/np.abs(np.sum(spacing[1,:]))
        ims = []
        for i in range(vol_ims.shape[2]):
            vol_im = scipy.misc.imresize(
                vol_ims[:,:,i], (
                    int(vol_ims.shape[0]*spc_ratio),
                    int(vol_ims.shape[1])
                ), interp="bicubic"
            )
            seg_im = scipy.misc.imresize(
                seg_ims[:,:,i], (
                    int(vol_ims.shape[0]*spc_ratio),
                    int(vol_ims.shape[1])
                ), interp="nearest"
            )
            sim = scipy.misc.imresize(
                seg[:,:,i], (
                    int(vol_ims.shape[0]*spc_ratio),
                    int(vol_ims.shape[1])
                ), interp="nearest"
            )
            viz_im = overlay(vol_im, seg_im, sim, alpha)
            ims.append(viz_im)
            if out_path:
                fpath = os.path.join(out_path,'{:05d}.png'.format(i))
                imwrite(str(fpath), viz_im)
        viz_ims = np.stack(ims)
    #网格显示
    n = int(np.shape(viz_ims)[0]**0.5) - 2
    fig,axes = plt.subplots(n,n,figsize=(100,100))
    k = 0
    for i in range(n):
        for j in range(n):
            axes[i][j].imshow(viz_ims[k])
            k += 1
    output = os.path.join(ROOT_PATH,'output')
    if not os.path.exists(output):
        os.mkdir(output)
    plt.savefig(os.path.join(output,str(cid)+'.png'))
    plt.show()


#显示图像
def imshow(title, imgs, shape=None, subtitle=None, cmap=None, transpose=False, pause=0.001, pltshow=True):
    if type(imgs) is tuple:
        num = len(imgs)
        if shape is not None:
            assert shape[0] * shape[1] == num
        else:
            shape = (1, num)
        
        if type(subtitle) is not tuple:
            subtitle = (subtitle,) * num
        else:
            assert len(subtitle) == num
        
        if type(cmap) is not tuple:
            cmap = (cmap,) * num
        else:
            assert len(cmap) == num
        
        fig = plt.figure(num=title, figsize=(shape[1] * 3, shape[0] * 3 + 0.5))
        fig.clf()
        fig.suptitle(title)
        
        fig.subplots(shape[0], shape[1], sharex=True, sharey=True)
        axes = fig.get_axes()
        
        for i in range(shape[0]):
            for j in range(shape[1]):
                idx = i * shape[1] + j
                axes[idx].set_title(subtitle[idx])
                
                cm = cmap[idx]
                img = imgs[idx]
                if cmap[idx] is None and len(img.shape) == 3:
                    if img.shape[0] == 1 or len(img.shape) == 2:
                        cm = 'gray'
                        if len(img.shape) == 3 and img.shape[0] == 1:
                            img = img.reshape((img.shape[1], img.shape[2]))
                    elif img.shape[0] == 3:
                        img = img.transpose((1, 2, 0))
                axes[idx].imshow(img, cm)
    else:
        if transpose:
            imgs = imgs.transpose((1, 2, 0))
        plt.figure(num=title)
        plt.suptitle(title)
        plt.title(subtitle)
        plt.imshow(imgs, cmap)
    if pltshow:
        plt.ion()
        plt.show()
        plt.pause(pause)
    return plt.gcf()

            
if __name__ == '__main__':
    desc = "Overlay a case's segmentation and store it as a series of pngs"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "-c", "--case_id", required=True,
        help="The identifier for the case you would like to visualize"
    )
    parser.add_argument(
        "-d", "--destination", required=False,
        help="The location where you'd like to store the series of pngs"
    )
    parser.add_argument(
        "-u", "--upper_hu_bound", required=False, default=DEFAULT_HU_MAX,
        help="The upper bound at which to clip HU values"
    )
    parser.add_argument(
        "-l", "--lower_hu_bound", required=False, default=DEFAULT_HU_MIN,
        help="The lower bound at which to clip HU values"
    )
    parser.add_argument(
        "-p", "--plane", required=False, default=DEFAULT_PLANE,
        help=(
            "The plane in which to visualize the data"
            " (axial, coronal, or sagittal)"
        )
    )
    args = parser.parse_args()
    display(
        args.case_id, args.destination, 
        hu_min=args.lower_hu_bound, hu_max=args.upper_hu_bound,
        plane=args.plane
    )