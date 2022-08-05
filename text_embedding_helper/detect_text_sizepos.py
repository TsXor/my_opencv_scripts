import cv2,pickle,sys,json,base64
import numpy as np 

def morphopen(img,iternum):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # 矩形结构
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=iternum)
def morphclose(img,iternum):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # 矩形结构
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=iternum)

class box:
    def __init__(self, l, t, w, h, img, contour):
        self.left = l; self.right = l+w; self.top = t; self.bottom = t+h
        self.width = w; self.height = h
        self.info = (l,t,w,h)
        self.contour = contour
        self.array = img[self.top:self.top+h, self.left:self.left+w]
        arraysum = self.array.sum(axis=0)
        linefilter = np.where((arraysum > 0),1 , arraysum)
        linefilter_rs1 = np.delete(np.insert(linefilter, 0, 1^linefilter[0]),linefilter.shape[0])
        linefilter_diff = linefilter^linefilter_rs1
        self.linepos = np.nonzero(linefilter_diff)[0]
        self.linepos = np.insert(self.linepos, self.linepos.shape[0], linefilter.shape[0])
        self.initline = linefilter[0]
        self.lines = []
        for i in range(self.linepos.shape[0]-1):
            line = (self.linepos[i+1]-self.linepos[i],i%2^self.initline)
            self.lines.append(line)
        i1 = []; i0 = []
        for j in self.lines:
          if j[1] == 1:
            i1.append(j[0])
          if j[1] == 0:
            i0.append(j[0])
        if sum(i0) == 0:
          self.lineinfo = (sum(i1)/len(i1),sum(i1)/len(i1)*1.5)
        else:
          self.lineinfo = (sum(i1)/len(i1),sum(i1)/len(i1)+sum(i0)/len(i0))
    def rel2abs(self, point):
        return (point[0]+self.top, point[1]+self.left)
    def abs2rel(self, point):
        return (point[0]-self.top, point[1]-self.left)
    def drawresult(self,imgc):
        #print(self.linepos,self.initline,'\n',self.lines)
        cv2.drawContours(imgc,(self.contour,),-1,(255,255,0))  #第三个参数为-1代表画所有轮廓，其余值代表相应的轮廓
        cv2.line(imgc, (self.left, self.top), (self.right, self.top), (0,255,0))
        cv2.line(imgc, (self.left, self.bottom), (self.right, self.bottom), (0,255,0))
        for pos in self.linepos:
            abspos = self.rel2abs((0,pos))[1]
            cv2.line(imgc, (abspos, self.top), (abspos, self.bottom), (0,0,255))

img = pickle.loads(base64.b64decode(sys.stdin.read().encode())); cv2.bitwise_not(img,img)  #cv读取模式为BGR
imgmor = morphopen(morphclose(img,18),2); contours,hier=cv2.findContours(imgmor,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
imgc = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
txtboxes = []
output = []
for c in contours:
    x,y,w,h=cv2.boundingRect(c);  #寻找边界矩形
    txtbox = box(x,y,w,h,img,c)
    output.append((txtbox.right,txtbox.top,*txtbox.lineinfo))
#    txtbox.drawresult(imgc)
sys.stdout.write(json.dumps(output))
#cv2.imshow('findEdge',imgc)
#cv2.waitKey()
