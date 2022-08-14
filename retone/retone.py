try:
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
except ImportError:
    import Image
import numpy as np
import sys,cv2,getopt

canny_low = 100
canny_high = 200
highdiff = 50

argv = sys.argv[1:]
img_path = ''; img_smooth_path = ''; output_path = ''; output_diff_path = ''; output_edge_path = ''
help_str = \
'''retone.py
  --toned-image=<原图片路径>
  --smooth-image=<光滑后图片路径>
  --output=<结果图片输出路径>  (可选)
  --output-diff=<差分提取输出路径>  (可选)
  --output-edge=<边缘提取输出路径>  (可选)
'''
try:
  opts, args = getopt.getopt(argv, '-h', ['help', 'toned-image=', 'smooth-image=', 'output=', 'output-diff=', 'output-edge='])
except getopt.GetoptError:
  print(help_str); sys.exit(2)
for opt, arg in opts:
  if opt in ("-h", "--help"):
    print(help_str); sys.exit()
  elif opt == '--toned-image':
    img_path = arg
  elif opt == '--smooth-image':
    img_smooth_path = arg
  elif opt == '--output':
    output_path = arg
  elif opt == '--output-diff':
    output_diff_path = arg
  elif opt == '--output-edge':
    output_edge_path = arg
if not img_path:
  print('缺少 --toned-image'); sys.exit(2)
if not img_smooth_path:
  print('缺少 --smooth-image'); sys.exit(2)

def morphopen(img,ksize,iternum):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))  # 矩形结构
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=iternum)
def morphclose(img,ksize,iternum):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))  # 矩形结构
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=iternum)
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

#读取
img_pil = Image.open(img_path)
img_smooth_pil = Image.open(img_smooth_path)
img_pil = img_pil.convert('L')
img_smooth_pil = img_smooth_pil.convert('L')
img_cv = np.asarray(img_pil)
img_smooth_cv = np.asarray(img_smooth_pil)

#放缩
s1x = (img_cv.shape[1], img_cv.shape[0])
snx = (img_cv.shape[1]*2, img_cv.shape[0]*2)
img_resize_cv = cv2.resize(img_cv, dsize=snx)
img_resize_cv = cv2.resize(img_resize_cv, dsize=s1x)

imgdiff_cv = cv2.subtract(img_resize_cv, img_cv)
#imgdiff_cv = np.ceil(imgdiff_cv*1.5).astype(np.uint8)  #增强白色
#imgdiff_cv = np.where(imgdiff_cv>255, 255, imgdiff_cv)  #超过255的截在255
img_rough_cv = cv2.add(imgdiff_cv, img_smooth_cv)
img_rough_sharpen_cv = sharpen(img_rough_cv, sharpness=60) #锐化

#对平滑图取边缘
edges = cv2.Canny(img_smooth_cv,canny_low,canny_high,L2gradient=False)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
edges = cv2.dilate(edges, kernel, 1)

#用原图的边缘覆盖锐化的叠加图的边缘，因为边缘受锐化影响
img_rough_cv = np.where(edges==255, img_rough_cv, img_rough_sharpen_cv)

#康康怎么样
#edges_pil = Image.fromarray(edges)
#edges_pil.show()
#imgdiff_pil_RGB = Image.fromarray(imgdiff_cv)
#imgdiff_pil_RGB.show()
#img_rough_pil_RGB = Image.fromarray(img_rough_cv)
#img_rough_pil_RGB.show()

if output_path:
  img_rough_pil_RGB.save(output_path)
if output_diff_path:
  imgdiff_pil_RGB.save(output_diff_path)
if output_edge_path:
  edges_pil.save(output_edge_path)
