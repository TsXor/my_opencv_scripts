import cv2
import numpy as np

def transform(imgs,imgd):
    squash_size = 600
    #压缩图片使处理更快
    ratios = squash_size/max(imgs.shape[0], imgs.shape[1])
    ratiod = squash_size/max(imgd.shape[0], imgd.shape[1])
    dsizetups = (int(imgs.shape[1]*ratios), int(imgs.shape[0]*ratios))
    dsizetupd = (int(imgd.shape[1]*ratiod), int(imgd.shape[0]*ratiod))
    imgs_sq = cv2.resize(imgs,dsize=dsizetups)
    imgd_sq = cv2.resize(imgd,dsize=dsizetupd)  
    sift = cv2.SIFT_create()
    # 检测关键点
    kps, des_s = sift.detectAndCompute(imgs_sq,None)
    kpd, des_d = sift.detectAndCompute(imgd_sq,None)

    # 关键点匹配
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 6)
    search_params = dict(checks = 10)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des_s,des_d,k=2)

    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
    # 把good中的左右点分别提出来找单应性变换
    pts_src = np.float32([ kps[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    pts_dst = np.float32([ kpd[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
    pts_src = pts_src/ratios
    pts_dst = pts_dst/ratiod

    # 单应性变换
    M, mask = cv2.findHomography(pts_src, pts_dst, cv2.RANSAC, 5.0)

    im_out = cv2.warpPerspective(imgs, M, (imgd.shape[1],imgd.shape[0]))
    return im_out
    #cv2.imshow('show', im_out)
    #cv2.waitKey(0)