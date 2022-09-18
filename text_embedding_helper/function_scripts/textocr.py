import cv2
import numpy as np
from PIL import Image
from lib_scripts.cvutils import *
import lib_scripts.UOCRbackend as UOCR

ocr_name = None
ocr_object = None

# 可调常量
THRESH_SMALL = 60
TEXT_SIZE_MIN = (20, 20)  #w>=20 and h>=20
TEXT_SIZE_MAX = (100, 500)  #w<=100 and h<=500

# 根据可调常量生成的具体参数常量
BLACK_THRESH = THRESH_SMALL
WHITE_THRESH = 255 - THRESH_SMALL
TEXT_SELECTOR_MIN = lambda c: (size(c)[0]>=TEXT_SIZE_MIN[0] and size(c)[1]>=TEXT_SIZE_MIN[1])
TEXT_SELECTOR_MAX = lambda c: (size(c)[0]<=TEXT_SIZE_MAX[0] and size(c)[1]<=TEXT_SIZE_MAX[1])

def select_contours(img, selector=(lambda x: True), fill=True):
    cnts = outer_contours(img)
    cnts = [c for c in cnts if selector(c)]
    selected = np.zeros(img.shape, dtype=np.uint8)
    fillp = -1 if fill else 1
    cv2.drawContours(selected, cnts, -1, (255,255,255), fillp)
    return selected

def size(c):  #仅仅是为了写起来短 :)
    x, y, w, h = cv2.boundingRect(c)
    return (w, h)

def load(ocr, lang):
    global ocr_name, ocr_object
    ocr_name = ocr
    ocr_class = getattr(UOCR, ocr)
    ocr_object = ocr_class(lang=lang)

def rectext(im, det):
    boxes = ocr_object.getbox(det)

    texts = []
    kernel = np.ones((3, 3), np.uint8)
    mask = np.zeros(im.shape, dtype=np.uint8)
    for box in boxes:
        smask = np.zeros(im.shape, dtype=np.uint8)
        x1, x2, y1, y2 = box
        cv2.rectangle(smask, (x1, y1), (x2, y2), (255, 255, 255), -1)
        cv2.rectangle(mask, (x1, y1), (x2, y2), (255, 255, 255), -1)
        sdet = immask(det, smask)
        sdet = cv2.dilate(sdet, kernel)
        stext = immask(im, sdet)
        texts.append(stext)
    det = immask(det, mask)
    cover = cv2.dilate(det, kernel)

    return texts, cover


color_ranges = [(0, BLACK_THRESH), (WHITE_THRESH, 255)]
txtcolors = [(0, 255), (255, 0)]
def main_api(im, ocr='easyocr', lang='ja'):
    if ocr_name != ocr:
        load(ocr, lang)

    edge = canny_bs(im, 245, 250, 50)
    kernel = np.ones((3, 3), np.uint8)
    edge = cv2.morphologyEx(edge, cv2.MORPH_CLOSE, kernel)
    edge_mask = select_contours(edge, TEXT_SELECTOR_MAX)
    edge_mask = cv2.dilate(edge_mask, kernel, iterations=2)
    edge_mask = select_contours(edge_mask, TEXT_SELECTOR_MIN)

    im_queue = [immask((cim := cv2.inRange(im, *cr)), select_contours(cim, TEXT_SELECTOR_MAX)) for cr in color_ranges]
    det_queue = [immask(sim, edge_mask) for sim in im_queue]
    results = [(*rectext(sim, sdet), txtcolor) for sim, sdet, txtcolor in zip(im_queue, det_queue, txtcolors)]

    return results
