# Window implementation for Systray
# Window implementation of a systray
# Mostly taken from: http://www.brunningonline.net/simon/blog/archives/SysTrayIcon.py.html
# Source credits goes to: Simon Brunning, Mark Hammond's

from plyer.facades import Systray
from os.path import isfile
import win32gui
import win32gui_struct
import win32api
import win32con


class WindowsSystray(Systray):

    # implementation
    def _configure(self):
        self._register()
        self._refresh()

    def _quit(self):
        win32gui.DestroyWindow(self._hwnd)

    def _run(self):
        win32gui.PumpMessages()

    def _register(self):
        if hasattr(self, '_register_done'):
            return
        self._notify_id = None
        message_map = {
               win32gui.RegisterWindowMessage('TaskbarCreated'): self._mm_restart,
               win32con.WM_DESTROY: self._mm_destroy,
               win32con.WM_COMMAND: self._mm_command,
               win32con.WM_USER + 20: self._mm_notify }
        window_class = win32gui.WNDCLASS()
        handle = window_class.hInstance = win32gui.GetModuleHandle(None)
        window_class.lpszClassName = self._class_name
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        window_class.hbrBackground = win32con.COLOR_WINDOW
        window_class.lpfnWndProc = message_map
        atom = win32gui.RegisterClass(window_class)

        # create
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self._hwnd = win32gui.CreateWindow(atom, self._class_name,
                style, 0, 0,
                win32con.CW_USEDEFAULT,win32con.CW_USEDEFAULT,
                0, 0, handle, None)
        win32gui.UpdateWindow(self._hwnd)
        self._register_done = True

    def _refresh(self):
        # Try and find a custom icon
        hinst = win32gui.GetModuleHandle(None)
        if self._icon and isfile(self._icon):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst,
                                       self._icon,
                                       win32con.IMAGE_ICON,
                                       0,
                                       0,
                                       icon_flags)
        else:
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if self._notify_id:
            message = win32gui.NIM_MODIFY
        else:
            message = win32gui.NIM_ADD
        self._notify_id = (self._hwnd,
                          0,
                          win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
                          win32con.WM_USER+20,
                          hicon,
                          self._hover_text)
        win32gui.Shell_NotifyIcon(message, self._notify_id)

    # handle popup internal message
    def _mm_restart(self):
        self._refresh()

    def _mm_destroy(self, *args):
        nid = (self._hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)
        self._notify_id = None

    def _mm_notify(self, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_LBUTTONUP:
            self.on_click()

        elif lparam == win32con.WM_RBUTTONUP:
            self._show_menu()

    def _mm_command(self, hwnd, msg, wparam, lparam):
        option_id = win32gui.LOWORD(wparam)
        callback = self._option_ids.get(option_id)
        if callback:
            callback()

    def _show_menu(self):
        menu = win32gui.CreatePopupMenu()
        self._create_menu(menu, self._menu_options)
        x, y = win32gui.GetCursorPos()
        win32gui.SetForegroundWindow(self._hwnd)
        win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, x, y,
                0, self._hwnd, None)

    def _create_menu(self, menu, options, option_id=None):
        if option_id is None:
            self._option_ids = {}
            option_id = 1023

        for text, icon, action in reversed(options):
            if not icon:
                icon = 0
            if icon:
                icon = self._prepare_menu_icon(icon)
            if isinstance(action, (list, tuple)):
                submenu = win32gui.CreatePopupMenu()
                self._create_menu(submenu, action, option_id=option_id)
                item, extras = win32gui_struct.PackMENUITEMINFO(
                        text=text, hbmpItem=icon, hSubMenu=submenu)
            else:
                # there is an action!
                item, extras = win32gui_struct.PackMENUITEMINFO(
                        text=text, hbmpItem=icon, wID=option_id)
                self._option_ids[option_id] = action
                option_id += 1
            win32gui.InsertMenuItem(menu, 0, 1, item)

    def _prepare_menu_icon(self, icon):
        # First load the icon.
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        hicon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, ico_x, ico_y,
                win32con.LR_LOADFROMFILE)

        hdcBitmap = win32gui.CreateCompatibleDC(0)
        hdcScreen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = win32gui.SelectObject(hdcBitmap, hbm)

        # Fill the background.
        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)

        # unclear if brush needs to be feed.  Best clue I can find is:
        # "GetSysColorBrush returns a cached brush instead of allocating a new
        # one." - implies no DeleteObject
        # draw the icon
        win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0,
                win32con.DI_NORMAL)
        win32gui.SelectObject(hdcBitmap, hbmOld)
        win32gui.DeleteDC(hdcBitmap)

        return hbm


def instance():
    return WindowsSystray()

