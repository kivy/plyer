# -- coding: utf-8 --

__all__ = ('WindowsBalloonTip', 'balloon_tip')


import time
import ctypes
from plyer.platforms.win.libs import win_api_defs
from plyer.compat import PY2
from threading import RLock


WS_OVERLAPPED = 0x00000000
WS_SYSMENU = 0x00080000
WM_DESTROY = 2
CW_USEDEFAULT = 8

LR_LOADFROMFILE = 16
LR_DEFAULTSIZE = 0x0040
IDI_APPLICATION = 32512
IMAGE_ICON = 1

NOTIFYICON_VERSION_4 = 4
NIM_ADD = 0
NIM_MODIFY = 1
NIM_DELETE = 2
NIM_SETVERSION = 4
NIF_MESSAGE = 1
NIF_ICON = 2
NIF_TIP = 4
NIF_INFO = 0x10
NIIF_USER = 4
NIIF_LARGE_ICON = 0x20


class WindowsBalloonTip(object):

    _class_atom = 0
    _wnd_class_ex = None
    _hwnd = None
    _hicon = None
    _balloon_icon = None
    _notify_data = None
    _count = 0
    _lock = RLock()

    @staticmethod
    def _get_unique_id():
        WindowsBalloonTip._lock.acquire()
        val = WindowsBalloonTip._count
        WindowsBalloonTip._count += 1
        WindowsBalloonTip._lock.release()
        return val

    def __init__(self, title, message, app_name, app_icon='', timeout=10):
        ''' app_icon if given is a icon file.
        '''

        wnd_class_ex = win_api_defs.get_WNDCLASSEXW()
        class_name = 'PlyerTaskbar' + str(WindowsBalloonTip._get_unique_id())
        if PY2:
            class_name = class_name.decode('utf8')
        wnd_class_ex.lpszClassName = class_name
        # keep ref to it as long as window is alive
        wnd_class_ex.lpfnWndProc =\
            win_api_defs.WindowProc(win_api_defs.DefWindowProcW)
        wnd_class_ex.hInstance = win_api_defs.GetModuleHandleW(None)
        if wnd_class_ex.hInstance is None:
            raise Exception('Could not get windows module instance.')
        class_atom = win_api_defs.RegisterClassExW(wnd_class_ex)
        if class_atom == 0:
            raise Exception('Could not register the PlyerTaskbar class.')
        self._class_atom = class_atom
        self._wnd_class_ex = wnd_class_ex

        # create window
        self._hwnd = win_api_defs.CreateWindowExW(0, class_atom,
            '', WS_OVERLAPPED, 0, 0, CW_USEDEFAULT,
            CW_USEDEFAULT, None, None, wnd_class_ex.hInstance, None)
        if self._hwnd is None:
            raise Exception('Could not get create window.')
        win_api_defs.UpdateWindow(self._hwnd)

        # load icon
        if app_icon:
            icon_flags = LR_LOADFROMFILE | LR_DEFAULTSIZE
            hicon = win_api_defs.LoadImageW(None, app_icon, IMAGE_ICON, 0, 0,
                                            icon_flags)
            if hicon is None:
                raise Exception('Could not load icon {}'.
                                format(icon_path_name))
            self._balloon_icon = self._hicon = hicon
        else:
            self._hicon = win_api_defs.LoadIconW(None,
                ctypes.cast(IDI_APPLICATION, win_api_defs.LPCWSTR))
        self.notify(title, message, app_name)
        if timeout:
            time.sleep(timeout)

    def __del__(self):
        self.remove_notify()
        if self._hicon is not None:
            win_api_defs.DestroyIcon(self._hicon)
        if self._wnd_class_ex is not None:
            win_api_defs.UnregisterClassW(self._class_atom,
                                          self._wnd_class_ex.hInstance)
        if self._hwnd is not None:
            win_api_defs.DestroyWindow(self._hwnd)

    def notify(self, title, message, app_name):
        ''' Displays a balloon in the systray. Can be called multiple times
        with different parameter values.
        '''
        self.remove_notify()
        # add icon and messages to window
        hicon = self._hicon
        flags = NIF_TIP | NIF_INFO
        icon_flag = 0
        if hicon is not None:
            flags |= NIF_ICON
            # if icon is default app's one, don't display it in message
            if self._balloon_icon is not None:
                icon_flag = NIIF_USER | NIIF_LARGE_ICON
        notify_data = win_api_defs.get_NOTIFYICONDATAW(0, self._hwnd,
            id(self), flags, 0, hicon, app_name, 0, 0, message,
            NOTIFYICON_VERSION_4, title, icon_flag, win_api_defs.GUID(),
            self._balloon_icon)

        self._notify_data = notify_data
        if not win_api_defs.Shell_NotifyIconW(NIM_ADD, notify_data):
            raise Exception('Shell_NotifyIconW failed.')
        if not win_api_defs.Shell_NotifyIconW(NIM_SETVERSION,
                                              notify_data):
            raise Exception('Shell_NotifyIconW failed.')

    def remove_notify(self):
        '''Removes the notify balloon, if displayed.
        '''
        if self._notify_data is not None:
            win_api_defs.Shell_NotifyIconW(NIM_DELETE, self._notify_data)
            self._notify_data = None


def balloon_tip(**kwargs):
    WindowsBalloonTip(**kwargs)
