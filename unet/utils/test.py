
from niiutils import load_case,get_case_path
from visualize import hu_to_grayscale,overlay,class_to_color
import numpy as np
import matplotlib.pyplot as plt

def test_load_case(cid):
    '''
    测试加载cid数据
    '''

    vol,seg = load_case(cid)
    a = hu_to_grayscale(vol.get_data(),-512,512)
    b = class_to_color(seg.get_data().astype(np.int32),[255,0,0], [0,0,255])
    c = overlay(a,b,seg.get_data().astype(np.int32),0.3)
    print(c[0])
    fig = plt.figure()
    
    plt.imshow(c[0])
    plt.show()
if __name__ == '__main__':
    test_load_case(1)

