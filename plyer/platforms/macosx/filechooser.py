'''
Mac OS X file chooser
---------------------
'''

from plyer.facades import FileChooser
from pyobjus import autoclass, objc_arr, objc_str
from pyobjus.dylib_manager import load_framework, INCLUDE

load_framework(INCLUDE.AppKit)
NSURL = autoclass('NSURL')
NSOpenPanel = autoclass('NSOpenPanel')
NSSavePanel = autoclass('NSSavePanel')
NSOKButton = 1


class MacFileChooser(object):
    '''A native implementation of file chooser dialogs using Apple's API
    through pyobjus.

    Not implemented features:
    * filters (partial, wildcards are converted to extensions if possible.
        Pass the Mac-specific "use_extensions" if you can provide
        Mac OS X-compatible to avoid automatic conversion)
    * multiple (only for save dialog. Available in open dialog)
    * icon
    * preview
    '''

    mode = "open"
    path = None
    multiple = False
    filters = []
    preview = False
    title = None
    icon = None
    show_hidden = False
    use_extensions = False

    def __init__(self, **kwargs):
        # Simulate Kivy's behavior
        for i in kwargs:
            setattr(self, i, kwargs[i])

    def run(self):
        panel = None
        if self.mode in ("open", "dir"):
            panel = NSOpenPanel.openPanel()
        else:
            panel = NSSavePanel.savePanel()

        panel.setCanCreateDirectories_(True)

        panel.setCanChooseDirectories_(self.mode == "dir")
        panel.setCanChooseFiles_(self.mode != "dir")
        panel.setShowsHiddenFiles_(self.show_hidden)

        if self.title:
            panel.setTitle_(objc_str(self.title))

        if self.mode != "save" and self.multiple:
            panel.setAllowsMultipleSelection_(True)

        # Mac OS X does not support wildcards unlike the other platforms.
        # This tries to convert wildcards to "extensions" when possible,
        # ans sets the panel to also allow other file types, just to be safe.
        if len(self.filters) > 0:
            filthies = []
            for f in self.filters:
                if type(f) == str:
                    if not self.use_extensions:
                        if f.strip().endswith("*"):
                            continue
                        pystr = f.strip().split("*")[-1].split(".")[-1]
                    filthies.append(objc_str(pystr))
                else:
                    for _ in f[1:]:
                        if not self.use_extensions:
                            if f.strip().endswith("*"):
                                continue
                            pystr = f.strip().split("*")[-1].split(".")[-1]
                        filthies.append(objc_str(pystr))

            ftypes_arr = objc_arr(filthies)
            panel.setAllowedFileTypes_(ftypes_arr)
            panel.setAllowsOtherFileTypes_(not self.use_extensions)

        if self.path:
            url = NSURL.fileURLWithPath_(self.path)
            panel.setDirectoryURL_(url)

        if panel.runModal():
            if self.mode == "save" or not self.multiple:
                return [panel.filename().UTF8String()]
            else:
                return [i.UTF8String() for i in panel.filenames()]
        return None


class MacOSXFileChooser(FileChooser):
    '''FileChooser implementation for Windows, using win3all.
    '''
    def _file_selection_dialog(self, **kwargs):
        return MacFileChooser(**kwargs).run()


def instance():
    return MacOSXFileChooser()
