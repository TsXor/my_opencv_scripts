### forceratio  
这个脚本需要作为模块使用，用于解决cv2.WINDOW_KEEPRATIO并不能使imshow窗口保持纵横比的问题  
原理：创建一个tkinter窗口，将imshow窗口设为此tkinter窗口的子窗口，tkinter窗口调整大小的同时调用回调函数调整imshow窗口的大小  
理论上也可用于其它任何窗口  
用法：  
```
import forceratio
forceratio_wnd = forceratio.start(window_class, window_name)
        #window_class: 目标窗口类名
        #window_name: 目标窗口名称
```
### forceratio_old
`forceratio`的另一种实现，使用pynput监听左键松开的事件并将窗口“扳回正轨”  
不用窗口套娃，但是bug较多，仅供参考（因为将pynput的监控线程放到新进程里的做法我个人感觉还挺有参考意义）  
用法：不推荐用，自行研究，提示：差不多，也是用start方法  
