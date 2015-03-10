'''
Windows file chooser
--------------------
'''

from plyer.facades import FileChooser
from win32com.shell import shell, shellcon
import os
import win32gui, win32con, pywintypes


class Win32FileChooser(object):
    """A native implementation of NativeFileChooser using the
    Win32 API on Windows.

    Not Implemented features (all dialogs):
    * preview
    * icon

    Not implemented features (in directory selection only - it's limited
    by Windows itself):
    * preview
    * window-icon
    * multiple
    * show_hidden
    * filters
    * path
    """

    path = None
    multiple = False
    filters = []
    preview = False
    title = None
    icon = None
    show_hidden = False

    def __init__(self, **kwargs):
        # Simulate Kivy's behavior
        for i in kwargs:
            setattr(self, i, kwargs[i])

    def run(self):
        try:
            if mode != "dir":
                args = {}

                if self.path:
                    atgs["InitialDir"] = os.path.dirname(self.path)
                    args["File"] = os.path.splitext(os.path.dirname(self.path))[0]
                    args["DefExt"] = os.path.splitext(os.path.dirname(self.path))[1]
                args["Title"] = self.title if self.title else "Pick a file..."
                args["CustomFilter"] = 'Other file types\x00*.*\x00'
                args["FilterIndex"] = 1

                filters = ""
                for f in self.filters:
                    if type(f) == str:
                        filters += (f + "\x00") * 2
                    else:
                        filters += f[0] + "\x00" + ";".join(f[1:]) + "\x00"
                args["Filter"] = filters

                flags = win32con.OFN_EXTENSIONDIFFERENT | win32con.OFN_OVERWRITEPROMPT
                if self.multiple:
                    flags |= win32con.OFN_ALLOWmultiple | win32con.OFN_EXPLORER
                if self.show_hidden:
                    flags |= win32con.OFN_FORCESHOWHIDDEN
                args["Flags"] = flags

                if self.mode == "open":
                    self.fname, self.customfilter, self.flags = win32gui.GetOpenFileNameW(**args)
                elif self.mode == "save":
                    self.fname, self.customfilter, self.flags = win32gui.GetSaveFileNameW(**args)

                if self.fname:
                    if self.multiple:
                        seq = str(self.fname).split("\x00")
                        dir_n, base_n = seq[0], seq[1:]
                        self.selection = [os.path.join(dir_n, i) for i in base_n]
                    else:
                        self.selection = str(self.fname).split("\x00")
            else:
                # From http://timgolden.me.uk/python/win32_how_do_i/browse-for-a-folder.html
                pidl, display_name, image_list = shell.SHBrowseForFolder(
                win32gui.GetDesktopWindow(), None,
                self.title if self.title else "Pick a folder...", 0, None, None)
                self.selection = [str(shell.SHGetPathFromIDList (pidl))]

            return self.selection
        except (RuntimeError, pywintypes.error):
            return None

class WinFileChooser(FileChooser):
    """FileChooser implementation for Windows, using win3all.
    """
    def _file_selection_dialog(self, **kwargs):
        return Win32FileChooser(**kwargs).run()


def instance():
    return WinFileChooser()
