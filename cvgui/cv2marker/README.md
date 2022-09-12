### cv2marker
这个脚本是一个UI，如其名，你可以用它标记出你想要的区域，然后它会以列表的形式返回已标记出的区域。  
用法：  
1. 直接使用  
用法：  
```
cv2marker.py  <图片文件路径>
```
注：仅供测试，不提供保存区域的功能  

2. 当模块用  
用法：
```
新建一个窗口
newImageWindow(window_name, window_size, imagefile, zonecallback):
        #window_name: 字符串，窗口名
        #window_size: 分数，窗口占整个屏幕的比例
        #imagefile: 字符串，要显示的图片的路径
        #zonecallback: 函数名，选中某个已经划定的区域时调用的函数，调用时提供的参数为选中的区域对象
```
使用例：`test.py`（与`cv2marker.py`在同一路径）
```python
import cv2marker
import sys
def zone_callback(zone):
    print(window.zones)
    print('左边界：x='+str(window.zones[zone].left))
    print('右边界：x='+str(window.zones[zone].right))
    print('上边界：y='+str(window.zones[zone].top))
    print('下边界：y='+str(window.zones[zone].bottom))
def zucb(event):
    print('event: %s'%event)
if __name__ == '__main__':
    window = cv2marker.newImageWindow('image', 7/8, sys.argv[1], zone_callback, zucb)
    window.mainloop()
```
```
test.py  <图片文件路径>
```
注：创建一个newImageWindow类的对象后，要执行mainloop方法才能让其窗口存续（即不执行mainloop窗口就会一闪而过）。当然也有其他办法，比如将这个对象的窗口设为其他窗口的子窗口。这个的运用方式很像tkinter的mainloop，故名。（没错，和tk的mainloop一样，在窗口关闭之前，mainloop之后的代码不会被执行！）  
  
这是另一个使用例，带json即时保存功能
```python
import cv2marker
import sys,os
import json
def zone_callback(zone):
    print(window.zones)
    print('左边界：x='+str(window.zones[zone].left))
    print('右边界：x='+str(window.zones[zone].right))
    print('上边界：y='+str(window.zones[zone].top))
    print('下边界：y='+str(window.zones[zone].bottom))
def zucb(event):
    print('event: %s'%event)
    zonelist = window.save_list()
    with open(jsonfile,'w') as f:
        json.dump(zonelist,f)
if __name__ == '__main__':
    window = cv2marker.newImageWindow('image', 7/8, sys.argv[1], zone_callback, zucb)
    jsondir = os.path.split(sys.argv[0])[0]+'\\json_output'
    os.system('mkdir %s'%jsondir)
    jsonfile = jsondir+'\\'+os.path.split(sys.argv[1])[1]+'.json'
    print('json保存在：'+jsonfile)
    if os.path.isfile(jsonfile):
        with open(jsonfile,'r') as f:
            zonelist = json.load(f)
            window.load_list(zonelist)
    window.mainloop()
```
