# -- coding: utf-8 --
# Original from https://gist.github.com/wontoncc/1808234
# Modified from https://gist.github.com/boppreh/4000505

import os
import sys
import time

import win32con
import win32gui
from win32api import GetModuleHandle


class WindowsBalloonTip:

    def __init__(self, title, msg):
        message_map = {win32con.WM_DESTROY: self.OnDestroy, }
        # Register the Window class.
        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map    # could also specify a wndproc.
        class_atom = win32gui.RegisterClass(wc)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(class_atom, "Taskbar", style,
                                          0, 0, win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT, 0, 0,
                                          hinst, None)
        win32gui.UpdateWindow(self.hwnd)
        icon_path_name = os.path.abspath(os.path.join(sys.path[0],
                                                      "balloontip.ico"))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
            hicon = win32gui.LoadImage(hinst, icon_path_name,
                                       win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY,
                                  (self.hwnd, 0, win32gui.NIF_INFO,
                                   win32con.WM_USER+20, hicon,
                                   "Balloon  tooltip", msg, 200, title))
        # self.show_balloon(title, msg)
        time.sleep(10)
        win32gui.DestroyWindow(self.hwnd)
        win32gui.UnregisterClass(class_atom, hinst)

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # Terminate the app.


def balloon_tip(title, msg):
    w = WindowsBalloonTip(title, msg)
