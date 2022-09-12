#Credits
#https://github.com/jrosebr1/color_transfer/blob/master/color_transfer/__init__.py -> The original form of gray_lightness_transfer
#https://blog.csdn.net/HELLOWORLD_x/article/details/115014457
#https://github.com/XuPeng23/CV/tree/main/Difference%20Detection%20In%20Similar%20Images

import gray_lightness_transfer as glt
import picture_homography_undiff as phu
try:
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
except ImportError:
    import Image
import numpy as np
import sys,cv2

imgs_pil = Image.open(sys.argv[1])
imgd_pil = Image.open(sys.argv[2])
imgs_pil_RGB = imgs_pil.convert("RGB")
imgd_pil_RGB = imgd_pil.convert("RGB")
imgs_cv_BGR = cv2.cvtColor(np.asarray(imgs_pil_RGB), cv2.COLOR_RGB2BGR)
imgd_cv_BGR = cv2.cvtColor(np.asarray(imgd_pil_RGB), cv2.COLOR_RGB2BGR)

imgs_cv_BGR = phu.transform(imgs_cv_BGR, imgd_cv_BGR)
imgs_cv_BGR = glt.lightness_transfer(imgd_cv_BGR, imgs_cv_BGR)
imgdiff_cv_BGR = imgs_cv_BGR - imgd_cv_BGR

imgdiff_pil_RGB = Image.fromarray(cv2.cvtColor(imgdiff_cv_BGR, cv2.COLOR_BGR2RGB))
imgdiff_pil_RGB.show()