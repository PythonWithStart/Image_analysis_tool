"""
图片修复
https://zhuanlan.zhihu.com/p/138169619
"""
"""
模糊图片处理清晰
"""

import cv2
import numpy as np

# image = cv2.imread('weixin_20210426213826.jpg')
# sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
# sharpen = cv2.filter2D(image, -1, sharpen_kernel)
#
# cv2.imshow('sharpen', sharpen)
# cv2.waitKey()

import numpy as np
import cv2

img = cv2.imread('weixin_20210426213826.jpg')
blur = cv2.blur(img, (5, 5))
blur = cv2.medianBlur(img, 5)
# 第三个参数为0是为了让高斯核自己计算标准差
blur = cv2.GaussianBlur(img, (5, 5), 0)
# 9邻域直径，两个75分别是空间高斯函数标准差，灰度值相似性高斯函数标准差
blur = cv2.bilateralFilter(img, 9, 75, 75)
mask = cv2.resize(blur, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
cv2.imshow('image', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
