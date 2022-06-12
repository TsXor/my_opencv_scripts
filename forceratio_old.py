import win32gui, win32con, pynput, time
from multiprocessing import Process

#用法：window_forceratio = forceratio.start(<window name>, <windowclass>)  返回子进程

def start(window_name, window_class):
    monitor_obj = window_monitor(window_name, window_class)
    monitor_obj.subproc.start()
    return monitor_obj.subproc

class SubProcess(Process):
    def __init__(self, mousecallback):
        Process.__init__(self)
        self.mcb = mousecallback
    def run(self):
        print('subp created')
        with pynput.mouse.Listener(on_click=self.mcb) as listener:
            listener.join()

class window_monitor:
    #在自己的电脑上测试发现，cv2.WINDOW_KEEPRATIO并未起到应有的作用，窗口的长宽比例仍然可以改变
    #因此此处耍个小聪明，使用pynput监控鼠标左键松开的事件，此事件发生时检查窗口大小，并将窗口缩小到原比例
    #原理很简单，改窗口的大小一般情况下要用到鼠标拖动，除非...你用win32gui改的
    def __init__(self, window_class, window_name):
        self.sys_wnd_handle = win32gui.FindWindow(window_class, window_name)
        self.window_rect = win32gui.GetWindowRect(self.sys_wnd_handle)
        self.winsize = (self.window_rect[2]-self.window_rect[0], self.window_rect[3]-self.window_rect[1])
        self.subproc = SubProcess(self.pynput_mouse_click)
    def pynput_mouse_click(self, x, y, button, pressed):
        print('clicked')
        if not pressed:
            if not win32gui.GetForegroundWindow() == self.sys_wnd_handle:
                return
            time.sleep(0.5)    #防止执行时窗口大小还未调整
            self.last_window_rect = self.window_rect
            self.last_winsize = self.winsize
            self.window_rect = win32gui.GetWindowRect(self.sys_wnd_handle)
            if self.window_rect[0] < 0 or self.window_rect[1] < 0 or self.window_rect[2] < 0 or self.window_rect[3] < 0:
                return
            print(self.last_window_rect)
            print(self.window_rect)
            self.winsize = (self.window_rect[2]-self.window_rect[0], self.window_rect[3]-self.window_rect[1])
            print(self.last_winsize)
            print(self.winsize)
            if self.winsize[0] != self.last_winsize[0] and self.winsize[1] != self.last_winsize[1]:
                print('resize')
                scale = min(self.winsize[0]/self.last_winsize[0], self.winsize[1]/self.last_winsize[1])
                print(scale)
                self.winsize = (round(self.last_winsize[0]*scale), round(self.last_winsize[1]*scale))
                print(self.winsize)
                if self.window_rect[0] == self.last_window_rect[0] and self.window_rect[1] == self.last_window_rect[1]:    #LT
                    print('lt')
                    win32gui.SetWindowPos(self.sys_wnd_handle, 0, self.window_rect[0], self.window_rect[1], self.winsize[0], self.winsize[1], win32con.SWP_NOZORDER)
                elif self.window_rect[0] == self.last_window_rect[0] and self.window_rect[3] == self.last_window_rect[3]:    #LB
                    print('lb')
                    win32gui.SetWindowPos(self.sys_wnd_handle, 0, self.window_rect[0], self.window_rect[3]-self.winsize[1], self.winsize[0], self.winsize[1], win32con.SWP_NOZORDER)
                elif self.window_rect[1] == self.last_window_rect[1] and self.window_rect[2] == self.last_window_rect[2]:    #RT
                    print('rt')
                    win32gui.SetWindowPos(self.sys_wnd_handle, 0, self.window_rect[2]-self.winsize[0], self.window_rect[1], self.winsize[0], self.winsize[1], win32con.SWP_NOZORDER)
                elif self.window_rect[2] == self.last_window_rect[2] and self.window_rect[3] == self.last_window_rect[3]:    #RB
                    print('rb')
                    win32gui.SetWindowPos(self.sys_wnd_handle, 0, self.window_rect[2]-self.winsize[0], self.window_rect[3]-self.winsize[1], self.winsize[0], self.winsize[1], win32con.SWP_NOZORDER)
                else:
                    print('INFO: 此处窗口大小改变恐怕不是手动操作所致')
            elif self.winsize[0] != self.last_winsize[0] or self.winsize[1] != self.last_winsize[1]:
                print('dropback')
                self.window_rect = self.last_window_rect
                self.winsize = self.last_winsize
                win32gui.SetWindowPos(self.sys_wnd_handle, 0, self.last_window_rect[0], self.last_window_rect[2], self.last_winsize[0], self.last_winsize[1], win32con.SWP_NOZORDER)
