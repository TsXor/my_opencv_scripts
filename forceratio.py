import win32gui, win32con
import tkinter as tk

def start(window_class, window_name):
    container_wnd = tk.Tk()
    wndmon = window_monitor(window_class, window_name, container_wnd)
    container_wnd.mainloop()

class window_monitor:
    def __init__(self, window_class, window_name, tk_container_wnd):
        self.target_wnd_handle = win32gui.FindWindow(window_class, window_name)
        self.window_rect = win32gui.GetWindowRect(self.target_wnd_handle)
        self.winsize = (self.window_rect[2]-self.window_rect[0], self.window_rect[3]-self.window_rect[1])
        self.XYratio = self.winsize[0]/self.winsize[1]
        self.container_wnd_handle = tk_container_wnd.winfo_id()
        #print(self.container_wnd_handle)
        #print(self.target_wnd_handle)
        tk_container_wnd.title(window_name)
        tk_container_wnd.wm_title(window_name)
        tk_container_wnd.bind('<Configure>', self.window_resize)
        #print('夺舍')
        tk_container_wnd.geometry(str(self.winsize[0])+'x'+str(self.winsize[1])+'+'+str(self.window_rect[0])+'+'+str(self.window_rect[1]))
        win32gui.SetParent(self.target_wnd_handle, self.container_wnd_handle)
        #win32gui.ShowWindow(self.target_wnd_handle, win32con.SW_MAXIMIZE)
        win32gui.SetWindowPos(self.target_wnd_handle, 0, 0, 0, self.winsize[0], self.winsize[1], win32con.SWP_NOZORDER)
        self.window_width = self.winsize[0]
        self.window_height = self.winsize[1]
    def window_resize(self, event=None):
        if event is not None:
            self.forceratio(self.container_wnd_handle, self.target_wnd_handle)
    def forceratio(self, container, target):
        self.last_window_rect = self.window_rect
        self.last_winsize = self.winsize
        self.window_rect = win32gui.GetWindowRect(container)
        self.winsize = (self.window_rect[2]-self.window_rect[0], self.window_rect[3]-self.window_rect[1])
        if self.window_rect[0] < 0 or self.window_rect[1] < 0 or self.window_rect[2] < 0 or self.window_rect[3] < 0:
            return
        if self.winsize[0] == self.last_winsize[0] and self.winsize[1] == self.last_winsize[1]:
            return
        #print(self.last_window_rect)
        #print(self.window_rect)
        #print(self.last_winsize)
        #print(self.winsize)
        target_size = (round(min(self.winsize[0], self.winsize[1]*self.XYratio)), round(min(self.winsize[0], self.winsize[1]*self.XYratio)/self.XYratio))
        #print(target_size)
        paramqueue = [round((-self.window_rect[0]+self.window_rect[2]-target_size[0])/2), round((-self.window_rect[1]+self.window_rect[3]-target_size[1])/2), target_size[0], target_size[1]]
        win32gui.SetWindowPos(target, 0, paramqueue[0], paramqueue[1], paramqueue[2], paramqueue[3], win32con.SWP_NOZORDER)
