import sys,cv2,pickle,base64
import numpy as np
try:
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
except ImportError:
    import Image
from psd_tools import PSDImage


psd = PSDImage.open(sys.argv[1]); psdlayers = list(psd.descendants())
img = psdlayers[0].topil(); mask = psdlayers[1].topil(); maskpos = (psdlayers[1].top,psdlayers[1].left)
imgarray = np.asarray(img.convert("RGBA")); maskarray = np.asarray(mask.convert("RGBA"))
def padimgarray(img,size,pos):
  img_pad_vert = (maskpos[0]-1, size[0]-img.shape[0]+1-pos[0])
  img_pad_hori = (maskpos[1]-1, size[1]-img.shape[1]+1-pos[1])
  img_pad = np.pad(img,(img_pad_vert,img_pad_hori,(0,0)),'constant', constant_values=(0,0))
  return img_pad
def maskimgarray(img,mask,maskpos):
  img_noalpha = img[:,:,:3]
  mask_pad = padimgarray(mask,(img.shape[0],img.shape[1]),maskpos)
  mask_alpha_pad = np.expand_dims(mask_pad[:,:,3],axis=2)
  result = np.concatenate((img_noalpha,mask_alpha_pad),axis=2)
  return result
def erasezeroalpha(img,bg):
  bgcolor = [bg[0],bg[1],bg[2],255]
  bg = np.array([[bgcolor]],dtype = np.uint8)
  alpha = np.expand_dims(img[:,:,3],axis=2)
  a = alpha.astype('int16')-np.array([[[1]]],dtype = np.int16)
  b = np.right_shift(a,15)
  c = b+np.array([[[1]]],dtype = np.int16)
  zerofilter = c.astype('uint8')
  reversefilter = np.bitwise_xor(zerofilter,np.array([[[1]]],dtype = np.uint8))
  return img*zerofilter+bg*reversefilter
def cvtarray(img,option):
  return np.asarray(Image.fromarray(img.astype('uint8')).convert(option))
def binarray(img,threshold):
  result = cv2.threshold(cvtarray(img,'L'),threshold,255,cv2.THRESH_BINARY)
  return result[1]
layeredimgarray = erasezeroalpha(maskimgarray(imgarray,maskarray,maskpos),(255,0,255))
#layeredimg = Image.fromarray(binarray(layeredimgarray,100).astype('uint8')).convert('L')
#layeredimg = Image.fromarray(layeredimgarray.astype('uint8')).convert('L')
sys.stdout.write(base64.b64encode(pickle.dumps(binarray(layeredimgarray,100).astype('uint8'))).decode())
