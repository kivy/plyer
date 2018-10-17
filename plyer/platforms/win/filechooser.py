'''
Windows file chooser
--------------------
'''

from plyer.facades import FileChooser
from win32com.shell.shell import (
    SHBrowseForFolder as browse,
    SHGetPathFromIDList as get_path
)
import win32gui
import win32con
import pywintypes
from os.path import dirname, splitext, join


class Win32FileChooser(object):
    '''A native implementation of NativeFileChooser using the
    Win32 API on Windows.

    Not Implemented features (all dialogs):
    * preview
    * icon

    Not implemented features (in directory selection only - it's limited
    by Windows itself):
    * preview
    * window-icon

    Known issues:
    * non-existins folders such as: Network, Control Panel, My Computer, Trash,
      Library and likes will raise a COM error. The path does not exist, nor
      a user can open from or save to such path.
    '''

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
        self.selection = []
        try:
            if self.mode != "dir":
                args = {}

                if self.path:
                    args["InitialDir"] = dirname(self.path)
                    _, ext = splitext(self.path)
                    args["File"] = self.path
                    args["DefExt"] = ext

                args["Title"] = self.title if self.title else "Pick a file..."
                args["CustomFilter"] = 'Other file types\x00*.*\x00'
                args["FilterIndex"] = 1

                # e.g. open_file(filters=['*.txt', '*.py'])
                filters = ""
                for f in self.filters:
                    if type(f) == str:
                        filters += (f + "\x00") * 2
                    else:
                        filters += f[0] + "\x00" + ";".join(f[1:]) + "\x00"
                args["Filter"] = filters

                flags = win32con.OFN_EXTENSIONDIFFERENT
                flags |= win32con.OFN_OVERWRITEPROMPT

                if self.multiple:
                    flags |= win32con.OFN_ALLOWMULTISELECT
                    flags |= win32con.OFN_EXPLORER
                if self.show_hidden:
                    flags |= win32con.OFN_FORCESHOWHIDDEN

                args["Flags"] = flags

                # GetOpenFileNameW, GetSaveFileNameW will raise
                # pywintypes.error: (0, '...', 'No error message is available')
                # which is most likely due to incorrect type handling from the
                # win32gui side; return empty list in that case after exception
                if self.mode == "open":
                    self.fname, _, _ = win32gui.GetOpenFileNameW(**args)
                elif self.mode == "save":
                    self.fname, _, _ = win32gui.GetSaveFileNameW(**args)

                if self.fname:
                    if self.multiple:
                        seq = str(self.fname).split("\x00")
                        dir_n, base_n = seq[0], seq[1:]
                        self.selection = [
                            join(dir_n, i) for i in base_n
                        ]
                    else:
                        self.selection = str(self.fname).split("\x00")

            else:  # dir mode
                # From http://goo.gl/UDqCqo
                pidl, name, images = browse(  # pylint: disable=unused-variable
                    win32gui.GetDesktopWindow(),
                    None,
                    self.title if self.title else "Pick a folder...",
                    0, None, None
                )

                # pidl is None when nothing is selected
                # and e.g. the dialog is closed afterwards with Cancel
                if pidl:
                    self.selection = [str(get_path(pidl).decode('utf-8'))]

        except (RuntimeError, pywintypes.error):
            # ALWAYS! let user know what happened
            import traceback
            traceback.print_exc()
        return self.selection


class WinFileChooser(FileChooser):
    '''FileChooser implementation for Windows, using win3all.
    '''

    def _file_selection_dialog(self, **kwargs):
        return Win32FileChooser(**kwargs).run()


def instance():
    return WinFileChooser()
