# -*- coding=utf-8 -*-

import win32gui  
import win32con  
import time  

# 需要win32gui支持，下载地址https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/
  
class TestTaskbarIcon:  
    def __init__(self):  
          
        # 注册一个窗口类  
        wc = win32gui.WNDCLASS()  
        hinst = wc.hInstance = win32gui.GetModuleHandle(None)  
        wc.lpszClassName = "PythonTaskbarDemo"  
        wc.lpfnWndProc = {win32con.WM_DESTROY: self.OnDestroy,}  
        classAtom = win32gui.RegisterClass(wc)  
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU  
        self.hwnd = win32gui.CreateWindow( classAtom, "Taskbar Demo", style,  
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,  
                0, 0, hinst, None)  
        hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)  
        nid = (self.hwnd, 0, win32gui.NIF_ICON, win32con.WM_USER+20, hicon, "Demo")  
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)  
  
    def showMsg(self, title, msg):  
        # 原作者使用Shell_NotifyIconA方法代替包装后的Shell_NotifyIcon方法  
        # 据称是不能win32gui structure, 我稀里糊涂搞出来了.  
        # 具体对比原代码.  
        nid = (self.hwnd, # 句柄  
                0, # 托盘图标ID  
                win32gui.NIF_INFO, # 标识  
                0, # 回调消息ID  
                0, # 托盘图标句柄  
                "TestMessage", # 图标字符串  
                msg, # 气球提示字符串  
                0, # 提示的显示时间  
                title, # 提示标题  
                win32gui.NIIF_INFO # 提示用到的图标  
                )  
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)  
  
    def OnDestroy(self, hwnd, msg, wparam, lparam):  
        nid = (self.hwnd, 0)  
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)  
        win32gui.PostQuitMessage(0) # Terminate the app.     
      

def notify(title, msg):
     t = TestTaskbarIcon()  
     t.showMsg(title, get_current_time() + "\n当前价格 :  " + msg)  
     time.sleep(5)  
     win32gui.DestroyWindow(t.hwnd)

def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
  
if __name__ == '__main__':  
    notify("出来吧", "奥特曼!")
