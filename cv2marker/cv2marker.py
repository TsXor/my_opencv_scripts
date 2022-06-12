import cv2
import numpy as np
import sys, os, win32api, win32con
from copy import *

class zone:
    def __init__(self, pt1, pt2):
        self.left = min(pt1[0],pt2[0])
        self.right = max(pt1[0],pt2[0])
        self.top = min(pt1[1],pt2[1])
        self.bottom = max(pt1[1],pt2[1])
        if self.right == self.left or self.bottom == self.top:
            self.invalid = 1
        else:
            self.invalid = 0
    def miz(self, curmouse):
        if curmouse[0] in range (self.left, self.right) and curmouse[1] in range (self.top, self.bottom):
            return True
        else:
            return False

class newImageWindow:
    def __init__(self, window_name, window_size, imagefile, zonecallback, zonesupdatecallback):
        #window_name: 字符串，窗口的名字
        #window_size: 分数，窗口占整个屏幕的比例
        #imagefile: 字符串，要显示的图片的路径
        #zonecallback: 函数名，选中某个已经划定的区域时调用的函数，调用时提供的参数为选中的区域对象在列表中的序号
        #zonesupdatecallback: 函数名，区域列表更新时调用的函数，调用时提供的参数为操作（新建：'new'、删除：'del'）
        self.imgorig = cv2.imdecode(np.fromfile(imagefile, dtype=np.uint8), cv2.IMREAD_COLOR)
        print('INFO: 图片尺寸：%sx%s'%(self.imgorig.shape[1], self.imgorig.shape[0]))
        if len(self.imgorig.shape) == 2:
            self.img_init = cv2.cvtColor(self.imgorig, cv2.COLOR_GRAY2RGB); print('INFO: 此图片为黑白')
        else:
            self.img_init = self.imgorig.copy()
        self.img = self.img_init.copy()
        self.img_last = self.img.copy()
        self.window_name = window_name
        cv2.namedWindow(window_name, cv2.WINDOW_KEEPRATIO)
        cv2.imshow(window_name, self.img)
        self.imgX = self.img.shape[1]
        self.imgY = self.img.shape[0]
        screenX = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        screenY = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        if screenX<screenY:
            self.imgratio = screenX*window_size/self.imgX
        else:
            self.imgratio = screenY*window_size/self.imgY
        cv2.resizeWindow(window_name, round(self.imgX*self.imgratio), round(self.imgY*self.imgratio))
        cv2.setMouseCallback(window_name, self.mouse, [window_name, zonecallback])
        self.zucb = zonesupdatecallback
        self.zone_declaring = 0 #此变量表示是否正在划定区域，是为1，不是为0
        self.curzone = [] #临时变量，没用
        self.zones = [] #此列表中包含所有已划定的区域（“区域”是下面的“zone”类）
        self.last_chosen = -1 #最近一次选中的区域，没有则为-1
        self.winclass = 'Main HighGUI class'
    def save_list(self):
    #save_list可以将zones转化为纯列表，这样就可以以json格式保存zone信息
    #执行save_list，返回纯列表
        objlist = []
        for zone in self.zones:
            objlist.append([zone.left, zone.right, zone.top, zone.bottom])
        return objlist
    def load_list(self, objlist):
    #load_list可以根据纯列表创建zone对象
    #给load_list输入纯列表，zones中将添加对应的对象
        for obj in objlist:
            newz = zone((obj[0], obj[2]), (obj[1], obj[3]))
            self.zones.append(newz)
            cv2.rectangle(self.img_last, (obj[0], obj[2]), (obj[1], obj[3]), (0, 0, 255), 1)
        self.img = self.img_last.copy()
        cv2.imshow(self.window_name, self.img)
    def mainloop(self):
        while True:
            key_code = cv2.waitKey(1000)
            if cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE) < 1: #当窗口关闭时为-1，显示时为0
                break
            if key_code != -1:
                self.kbd(key_code)
    def kbd(self, key_code):
        #print('key {} pressed!!! value={}'.format(chr(key_code), key_code))
        if key_code == 8:
            if self.zone_declaring == 0:
                self.del_zone(self.last_chosen)
            else:
                self.curzone = []
                self.zone_declaring = 0
                self.img = self.img_last.copy()
                cv2.imshow(self.window_name, self.img)
    def mouse_in_zone(self, curmouse):
        if len(self.zones) == 0:
           return -1
        for i in range(len(self.zones)):
            if self.zones[i].miz(curmouse):
                return i
        return -1
    def add_zone(self, zone):
        if zone.invalid == 1:
            return 'invalid zone'; print('zone has 0 width/height, ignored')
        self.zones.append(zone)
        cv2.rectangle(self.img_last, (zone.left, zone.top), (zone.right, zone.bottom), (0, 0, 255), 1)
        self.img = self.img_last.copy()
        cv2.imshow(self.window_name, self.img)
        self.zucb('new')
    def del_zone(self, zonenum):
        if not zonenum in range(len(self.zones)):
            return
        self.zones.pop(zonenum)
        self.img_last = self.img_init.copy()
        self.last_chosen = -1
        for zone in self.zones:
            cv2.rectangle(self.img_last, (zone.left, zone.top), (zone.right, zone.bottom), (0, 0, 255), 1)
        self.img = self.img_last.copy()
        cv2.imshow(self.window_name, self.img)
        self.zucb('del')
    def mouse(self, event, x, y, flags, param):
        global zones
        window_name = param[0]
        zonecallback = param[1]
        if event == cv2.EVENT_LBUTTONDOWN:
            #xy = "%d,%d" % (x, y)
            #cv2.putText(self.img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255), thickness = 1)
            #cv2.imshow(window_name, self.img)
            if self.zone_declaring == 0:
                miz_zone_num = self.mouse_in_zone((x, y))
                if miz_zone_num != -1:
                    self.last_chosen = miz_zone_num
                    self.img = self.img_last.copy()
                    cv2.rectangle(self.img, (self.zones[miz_zone_num].left, self.zones[miz_zone_num].top), (self.zones[miz_zone_num].right, self.zones[miz_zone_num].bottom), (0, 255, 0), 1);
                    zonecallback(miz_zone_num)
                else:
                    cv2.circle(self.img, (x, y), 3, (0, 0, 255), thickness = -1)
                    self.zone_declaring = 1
                    self.curzone.append((x,y))
            else:
                cv2.circle(self.img, (x, y), 3, (0, 0, 255), thickness = -1)
                self.zone_declaring = 0
                self.curzone.append((x,y))
                zoneobj = zone(self.curzone[0], self.curzone[1])
                self.add_zone(zoneobj)
                self.curzone = []
        if event == cv2.EVENT_LBUTTONUP:
            cv2.imshow(window_name, self.img)
        if event == cv2.EVENT_MOUSEMOVE:
            if self.zone_declaring == 1:
                tmpzone = zone(self.curzone[0], (x, y))
                self.img = self.img_last.copy()
                cv2.rectangle(self.img, (tmpzone.left, tmpzone.top), (tmpzone.right, tmpzone.bottom), (0, 0, 255), 1);
                cv2.circle(self.img, self.curzone[0], 3, (0, 0, 255), thickness = -1)
                cv2.circle(self.img, (x, y), 3, (0, 0, 255), thickness = -1)
            if self.last_chosen != -1:
                cv2.rectangle(self.img, (self.zones[self.last_chosen].left, self.zones[self.last_chosen].top), (self.zones[self.last_chosen].right, self.zones[self.last_chosen].bottom), (0, 255, 0), 1);
            cv2.imshow(window_name, self.img)

def nothing(arg):
    pass
if __name__ == '__main__':
    window = newImageWindow('image', 7/8, sys.argv[1], nothing, nothing)
