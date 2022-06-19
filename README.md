# my_opencv_scripts
一些opencv有关的python脚本

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
newImageWindow(window_name, window_size, imagefile, zonecallback, zonesupdatecallback):
        #window_name: 字符串，窗口名
        #window_size: 分数，窗口占整个屏幕的比例
        #imagefile: 字符串，要显示的图片的路径
        #zonecallback: 函数名，选中某个已经划定的区域时调用的函数，调用时提供的参数为选中的区域对象
        #zonesupdatecallback: 函数名，“zones”列表更新时调用的函数，调用时提供的参数为列表本身
```
使用例：`test.py`（与`cv2marker.py`在同一路径）
```python
import cv2marker
import sys
def zone_callback(zone):
    print('左边界：x='+str(zone.left))
    print('右边界：x='+str(zone.right))
    print('上边界：y='+str(zone.top))
    print('下边界：y='+str(zone.bottom))
def zones_update_callback(zones):
    print(zones)
if __name__ == '__main__':
    window = cv2marker.newImageWindow('image', 7/8, sys.argv[1], zone_callback, zones_update_callback)
```
```
test.py  <图片文件路径>
```

### forceratio
这个脚本需要作为模块使用，用于解决cv2.WINDOW_KEEPRATIO并不能使imshow窗口保持纵横比的问题
原理：创建一个tkinter窗口，将imshow窗口设为此tkinter窗口的子窗口，tkinter窗口调整大小的同时调用回调函数调整imshow窗口的大小
理论上也可用于其它任何窗口
用法：
```
forceratio_wnd = forceratio.start(window_class, window_name)
        #window_class: 目标窗口类名
        #window_name: 目标窗口名称
```
