
import os
import nibabel as nib

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

'''
获取完整的case_id名称
'''
def get_full_case_id(cid):
    try:
        cid = int(cid)
        case_id = 'case_{:05d}'.format(cid)
    except ValueError:
        case_id = cid
    return case_id

'''
获取case的地址
'''
def get_case_path(cid):
    root = os.path.join(ROOT_PATH,'data')
    if not os.path.exists(root):
        raise IOError(
            'Data path,{},could not be resolved'.format(str(root))
        )
    case_id = get_full_case_id(cid)

    case_path = os.path.join(root,case_id)
    if not os.path.exists(case_path):
        raise ValueError(
        'Case could not be found {}'.format(case_path)
    )
    return case_path

def load_volume(cid):
    case_path = get_case_path(cid)
    vol = nib.load(os.path.join(case_path,'imaging.nii.gz'))
    return vol

def load_segmentation(cid):
    case_path = get_case_path(cid)
    seg = nib.load(os.path.join(case_path,'segmentation.nii.gz'))
    return seg


'''
加载case数据
'''
def load_case(cid):
    vol = load_volume(cid)
    seg = load_segmentation(cid)
    return vol,seg