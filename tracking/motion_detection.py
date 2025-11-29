# Louis Do
# 1002072156
# Windows 11
# Python 3.11.3
import numpy as np
from skimage.morphology import dilation, binary_closing, rectangle
from skimage.measure import label, regionprops

# function detectMotion is used to find the moving area within three frames by using the threshold as well as shape filtre
def detectMotion(f1, f2, f3, t=45, area=800):
    d1 = np.abs(f1 - f2)
    d2 = np.abs(f2 - f3)

    m = np.minimum(d1, d2)
    m = (m >= t).astype(np.uint8)
    m = binary_closing(m, rectangle(7, 7))
    m = dilation(m, rectangle(9, 9))
    m = m.astype(np.uint8)

    name = label(m)
    props = regionprops(name)

    count = []
    for r in props:
        if r.area >= area:
            count.append(r.bbox)

    return m * 255, count