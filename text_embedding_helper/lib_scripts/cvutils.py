import cv2
#import skimage
import numpy as np

BLACK = 0
WHITE = 255

def blur(img, ksize=15):
    assert ksize>=1
    ksize = round((ksize-1)/2)*2+1
    return cv2.GaussianBlur(img, (ksize,ksize), 0)

def blur_rb(img, ksize=15):
    assert ksize>=1
    ksize = round(ksize)
    return cv2.bilateralFilter(img, ksize, ksize*2, ksize/2)

def sharpen(img, sharpness=100, ktype=1):
  n = sharpness/100
  if ktype == 1:
    sharpen_op = np.array([[ 0,  -n  ,  0], \
                           [-n, 4*n+1, -n], \
                           [ 0,  -n  ,  0]], dtype=np.float32)
  if ktype == 2:
    sharpen_op = np.array([[-n,  -n,   -n], \
                           [-n, 8*n+1, -n], \
                           [-n,  -n,   -n]], dtype=np.float32)
  img_sharpen = cv2.filter2D(img, cv2.CV_32F, sharpen_op)
  img_sharpen = cv2.convertScaleAbs(img_sharpen)
  return img_sharpen

def canny_bs(img, low, high, force):
    img_bs = sharpen(blur_rb(blur(img, force/7.5), force/5), force)
    return cv2.Canny(img_bs, low, high, L2gradient=True)

#def skeletonize(img):
#    simg = np.where(img == 255, 0, 1)
#    ske = skimage.morphology.skeletonize(simg)
#    ske = ske.astype(np.uint8)*255
#    return ske

def outer_contours(img):
    contours, hier = cv2.findContours(img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    return [contours[i] for i in range(len(hier[0])) if hier[0][i][3]==-1]

def immask(img, mask):
    return cv2.bitwise_and(img, img, mask=mask)
