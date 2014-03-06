# -- coding: utf-8 --
# Original from https://gist.github.com/wontoncc/1808234
# Modified from https://gist.github.com/boppreh/4000505

import os
import sys
import time

import win32gui
from win32api import GetModuleHandle

WS_OVERLAPPED = 0x00000000
WS_SYSMENU = 0x00080000
WM_DESTROY = 2
CW_USEDEFAULT = 8

LR_LOADFROMFILE = 16
LR_DEFAULTSIZE = 0x0040

IMAGE_ICON = 1

IDI_APPLICATION = 32512

WM_USER = 1024

class WindowsBalloonTip:

    def __init__(self, title, message, app_name, app_icon, timeout=10):
        message_map = {WM_DESTROY: self.OnDestroy, }
        # Register the Window class.
        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map    # could also specify a wndproc.
        class_atom = win32gui.RegisterClass(wc)
        # Create the Window.
        style = WS_OVERLAPPED |  WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(class_atom, "Taskbar", style,
                                          0, 0, CW_USEDEFAULT,
                                          CW_USEDEFAULT, 0, 0,
                                          hinst, None)
        win32gui.UpdateWindow(self.hwnd)
        if app_icon:
            icon_path_name = app_icon
        else:
            icon_path_name = os.path.abspath(os.path.join(sys.path[0],
                                                      "balloontip.ico"))
        icon_flags = LR_LOADFROMFILE | LR_DEFAULTSIZE
        try:
            hicon = win32gui.LoadImage(hinst, icon_path_name,
                                       IMAGE_ICON, 0, 0, icon_flags)
        except:
            hicon = win32gui.LoadIcon(0, IDI_APPLICATION)
        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, WM_USER+20, hicon, "tooltip")
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY,
                                  (self.hwnd, 0, win32gui.NIF_INFO,
                                   WM_USER+20, hicon,
                                   "Balloon  tooltip", message, 200, title))
        # self.show_balloon(title, msg)
        time.sleep(timeout)
        win32gui.DestroyWindow(self.hwnd)
        win32gui.UnregisterClass(class_atom, hinst)

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # Terminate the app.


def balloon_tip(**kwargs):
    title = kwargs.get('title', '')
    message = kwargs.get('message', '')
    app_name = kwargs.get('app_name', '')
    app_icon = kwargs.get('app_icon', '')
    timeout = kwargs.get('timeout', 10)
    w = WindowsBalloonTip(**kwargs)
