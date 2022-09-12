import cv2
import numpy as np
from lib_scripts.cvutils import *
import easyocr


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
    im4scan = np.where(rimg2==255, im, 255)
    im4scan = np.where(im4scan>=128, 255, 0)
    im4scan = im4scan.astype('uint8')

    reader = easyocr.Reader(['ja'], recognizer=False) # this needs to run only once to load the model into memory
    result = reader.detect(im4scan)
    boxes = result[0][0]

    rimg3 = np.zeros(edge.shape, dtype=np.uint8)
    for box in boxes:
        x1, x2, y1, y2 = box
        cv2.rectangle(rimg3, (x1, y1), (x2, y2), (255, 255, 255), -1)
    im4scan = np.where(rimg3==255, im4scan, 255)
    im4scan = cv2.bitwise_not(im4scan)
    im4scan = cv2.dilate(im4scan, np.ones((3,3), np.uint8), iterations=1)
    return im4scan
