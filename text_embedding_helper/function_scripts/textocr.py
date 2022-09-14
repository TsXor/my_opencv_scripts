import cv2
import numpy as np
from lib_scripts.cvutils import *
import easyocr
reader = easyocr.Reader(['ja'], recognizer=False) # this needs to run only once to load the model into memory


def main_api(im):
    edge = canny_bs(im, 245, 250, 50)
    kernel = np.ones((4, 4), np.uint8)
    edge = cv2.dilate(edge, np.ones((4,4), np.uint8), iterations=1)
    rimg1 = np.zeros(edge.shape, dtype=np.uint8)
    for c in outer_contours(edge):
        x, y, w, h = cv2.boundingRect(c)
        if not (w<=80 and h<=500):
            continue
        cv2.drawContours(rimg1, [c], -1, (255,255,255), -1)
    rimg1 = cv2.dilate(rimg1, np.ones((4,4), np.uint8), iterations=2)
    rimg2 = np.zeros(edge.shape, dtype=np.uint8)
    for c in outer_contours(rimg1):
        x, y, w, h = cv2.boundingRect(c)
        if (w<=20 and h<=20):
            continue
        cv2.drawContours(rimg2, [c], -1, (255,255,255), -1)
    det = np.where(rimg2==255, im, 255)
    det = np.where(det>=128, 255, 0).astype('uint8')

    result = reader.detect(det)
    boxes = result[0][0]

    texts = []
    rimg = np.zeros(edge.shape, dtype=np.uint8)
    for box in boxes:
        nrimg = np.zeros(edge.shape, dtype=np.uint8)
        x1, x2, y1, y2 = box
        cv2.rectangle(nrimg, (x1, y1), (x2, y2), (255, 255, 255), -1)
        cv2.rectangle(rimg, (x1, y1), (x2, y2), (255, 255, 255), -1)
        sdet = np.where(nrimg==255, det, 255)
        sdet = cv2.bitwise_not(sdet)
        sdet = cv2.dilate(sdet, np.ones((3,3), np.uint8), iterations=1)
        stext = np.where(sdet==255, im, 255)
        stext = cv2.bitwise_not(stext)  # 反相
        texts.append(stext)

    det = np.where(rimg==255, det, 255)
    cover = cv2.dilate(cv2.bitwise_not(det), np.ones((3,3), np.uint8), iterations=1)

    return texts, cover
