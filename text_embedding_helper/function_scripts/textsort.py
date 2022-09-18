import json
from copy import copy
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


morphclose_iternum = 15
x_axis = 0; y_axis = 1


def sediment(arr, axis=0):  # “沉淀”，保留备用
    sediment = arr.sum(axis=axis)
    sediment = np.where((sediment > 0), 1, 0)
    sediment = sediment.tolist()
    state = sediment[0]
    bucket = [state, 0]
    result = []
    for i in sediment:
        if i == state:
            bucket[1] += 1
        else:
            result.append(copy(bucket))
            state = i
            bucket = [state, 1]
    result.append(copy(bucket))
    return result

def rectify(img):
    rects = np.zeros(img.shape, dtype=np.uint8)
    contours = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(rects, (x, y), (x+w, y+h), (255, 255, 255), -1)
    return rects

def acompare_range(a, b, error=(0.8, 1.25)):  # 带误差地比较a和b
    return a > b * error[0] and a < b * error[1]
def acompare_diff(a, b, error):  # 带误差地比较a和b
    return a > b - error and a < b + error

def bucket_sort(bucket):  # 这不是经典的“桶排序”，这只是“排序一个桶内的元素”
    assert bucket
    f = lambda zone: zone.axis
    return sorted(bucket, key=f, reverse=True)  # 反排，因为竖排文字从右到左

def avg(l):
    return sum(l)/len(l)

def zone_match(zone1, zone2):
    if not acompare_range(zone1.width, zone2.width):
        return False
    aw = (zone1.width+zone2.width)/2
    if not acompare_diff(zone1.top, zone2.top, aw*2):
        return False
    # 本来这里有个abs，但是下方的算法使我需要去掉它
    xdis = zone1.axis-zone2.axis
    if not acompare_range(xdis, aw, (0.5, 2.5)):
        return False
    return True

def match2chains(matches):
    r = list(range(len(matches)))
    chains = []
    while r:
        chain = []
        idx = r.pop(0)
        chain.append(idx)
        nextl = matches[idx]
        while nextl:
            idx = nextl[0]
            if idx not in r:
                break
            if idx in chain:
                break
            chain.append(idx)
            r.remove(idx)
            nextl = matches[idx]
        chains.append(chain)
    return chains

def bucket2info(bucket):
    bucket = bucket_sort(bucket)
    assert bucket
    if len(bucket) == 1:
        lineinfo = [(bucket[0].width, bucket[0].width * 1.5)]
        pos = (bucket[0].axis, bucket[0].top)
    else:
        l_width = [z.width for z in bucket]
        aw = avg(l_width)
        l_dis = [bucket[i - 1].axis - bucket[i].axis for i in range(1, len(bucket))]
        #lineinfo = [(l_width[i], l_dis[i]) for i in range(len(bucket) - 1)]
        #lineinfo.append((l_width[-1], l_width[-1] * 1.5))
        lineinfo = [(aw, l_dis[i]) for i in range(len(bucket) - 1)]
        lineinfo.append((aw, l_width[-1] * 1.5))
        l_top = [z.top for z in bucket]
        #at = avg(l_top)
        at = min(l_top)
        pos = (bucket[0].axis, at)
    return {"pos": pos, "lines": lineinfo}

def bucket_rect(bucket):
    bucket = bucket_sort(bucket)
    assert bucket
    l_top = [z.top for z in bucket]
    #t = round(avg(l_top))
    t = min(l_top)
    l_bottom = [z.bottom for z in bucket]
    b = max(l_bottom)
    l = bucket[-1].left
    r = bucket[0].right
    return (l, t, r - l, b - t)


class zone:
    def __init__(self, rect=None, contour=None):
        if rect:
            self.rect = rect
        if type(contour) != type(None):
            self.rect = cv2.boundingRect(contour)  # 寻找边界矩形
        l, t, w, h = self.rect
        self.left = l
        self.right = l + w
        self.top = t
        self.bottom = t + h
        self.width = w
        self.height = h
        self.axis = (self.left + self.right) / 2
    def imgslice(self, img):
        return img[self.top : self.top + h, self.left : self.left + w]
    def rel2abs(self, point):
        return (point[0] + self.top, point[1] + self.left)
    def abs2rel(self, point):
        return (point[0] - self.top, point[1] - self.left)
    def draw(self, img, color=(255, 0, 0)):
        l, t, w, h = self.rect
        cv2.rectangle(img, (l, t), (l + w, t + h), color, 1)
    def tag(self, img, color=(0, 255, 0), text=''):
        l, t, w, h = self.rect
        cv2.putText(img, text , (l, t), cv2.FONT_HERSHEY_COMPLEX, 1, color, 1)
    def __repr__(self):
        return "zone(rect=%s)" % repr(self.rect)

def main_api(texts, rim):
    if not texts:
        return [()], np.ones(rim.shape, dtype=np.uint8)*255
    show = np.zeros(texts[0].shape, dtype=np.uint8)
    contours = []
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))  # 只在竖直方向闭运算
    bucket_shelf = []
    for img in texts:
        show = np.where(img>0, img, show)
        imgmor = rectify(img)
        imgmor = cv2.morphologyEx(imgmor, cv2.MORPH_CLOSE, kernel, iterations=morphclose_iternum)
        contours += cv2.findContours(imgmor, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    showc = cv2.cvtColor(cv2.bitwise_not(show), cv2.COLOR_GRAY2RGB)

    # 提取文字信息
    zones = [zone(contour=c) for c in contours]
    zones = bucket_sort(zones)
    for i in range(len(zones)):
        z = zones[i]
        z.draw(showc)
        z.tag(showc, text=str(i))
    matches = [[j for j in range(i+1, len(zones)) if zone_match(zones[i], zones[j])] for i in range(len(zones))]
    chains = match2chains(matches)
    bucket_shelf = [[zones[i] for i in chain] for chain in chains]

    # 构造表
    sheet = []
    for bucket in bucket_shelf:
        info = bucket2info(bucket)
        l, t, w, h = bucket_rect(bucket)
        info.update({'rect':[(l, t), (l+w, t+h)]})
        cv2.rectangle(showc, (l, t), (l+w, t+h), (0, 255, 0), 1)
        imgslice = rim[t:t+h, l:l+w]
        row = [imgslice, '', json.dumps(info)]
        sheet.append(row)

    return sheet, showc
