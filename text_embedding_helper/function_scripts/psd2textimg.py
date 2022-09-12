import cv2
import numpy as np
from PIL import Image
from psd_tools import PSDImage
import click


def padimgarray(img,size,pos):
    img_pad_vert = (pos[0]-1, size[0]-img.shape[0]+1-pos[0])
    img_pad_hori = (pos[1]-1, size[1]-img.shape[1]+1-pos[1])
    img_pad = np.pad(img, (img_pad_vert, img_pad_hori, (0,0)), 'constant', constant_values=(0,0))
    return img_pad

def cvtarray(img,option):
    return np.asarray(Image.fromarray(img).convert(option))

def binarray(img,threshold):
    result = cv2.threshold(cvtarray(img,'L'),threshold,255,cv2.THRESH_BINARY)
    return result[1]


def main_api(inobj):
    # read PSD
    psd = inobj
    psdlayers = list(psd.descendants())
    Pimg = psdlayers[0].topil(); Pmask = psdlayers[1].topil()
    maskpos = (psdlayers[1].top,psdlayers[1].left)
    img = np.asarray(Pimg); mask = np.asarray(Pmask.convert("RGBA"))
    mask = padimgarray(mask, img.shape, maskpos)
    # get text area
    mask_alpha = mask[:,:,-1]
    txtimg = np.where(mask==0, 255, img)
    txtimg = binarray(txtimg, 128)
    #output
    result = txtimg
    return result