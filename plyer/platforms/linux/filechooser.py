'''
Linux file chooser
------------------
'''

from plyer.facades import FileChooser
from shutil import which
import os
import subprocess as sp
import time
import mimetypes

class SubprocessFileChooser:
    '''A file chooser implementation that allows using
    subprocess back-ends.
    Normally you only need to override _gen_cmdline, executable,
    separator and successretcode.
    '''

    executable = ""
    '''The name of the executable of the back-end.
    '''

    separator = "|"
    '''The separator used by the back-end. Override this for automatic
    splitting, or override _split_output.
    '''

    successretcode = 0
    '''The return code which is returned when the user doesn't close the
    dialog without choosing anything, or when the app doesn't crash.
    '''

    path = None
    multiple = False
    filters = []
    preview = False
    title = None
    icon = None
    show_hidden = False

    def __init__(self, *args, **kwargs):
        self._handle_selection = kwargs.pop(
            'on_selection', self._handle_selection
        )

        # Simulate Kivy's behavior
        for i in kwargs:
            setattr(self, i, kwargs[i])

    @staticmethod
    def _handle_selection(selection):
        '''
        Dummy placeholder for returning selection from chooser.
        '''
        return selection

    _process = None

    def _run_command(self, cmd):
        self._process = sp.Popen(cmd, stdout=sp.PIPE)
        while True:
            ret = self._process.poll()
            if ret is not None:
                if ret == self.successretcode:
                    out = self._process.communicate()[0].strip().decode('utf8')
                    return self._set_and_return_selection(
                        self._split_output(out))
                else:
                    return self._set_and_return_selection(None)
            time.sleep(0.1)

    def _set_and_return_selection(self, value):
        self.selection = value
        self._handle_selection(value)
        return value

    def _split_output(self, out):
        '''This methods receives the output of the back-end and turns
        it into a list of paths.
        '''
        return out.split(self.separator)

    def _gen_cmdline(self):
        '''Returns the command line of the back-end, based on the current
        properties. You need to override this.
        '''
        raise NotImplementedError()

    def run(self):
        return self._run_command(self._gen_cmdline())


class ZenityFileChooser(SubprocessFileChooser):
    '''A FileChooser implementation using Zenity (on GNU/Linux).

    Not implemented features:
    * show_hidden
    * preview
    '''

    executable = "zenity"
    separator = "|"
    successretcode = 0

    mime_type = {
        "doc": "application/msword",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "ppt": "application/vnd.ms-powerpoint",
        "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "xls": "application/vnd.ms-excel",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "pdf": "application/pdf",
        "zip": "application/zip",

        "text": "text/",
        "image": "image/",
        "video": "video/",
        "audio": "audio/",
        "application": "application/",
    }

    def _gen_cmdline(self):
        cmdline = [
            which(self.executable),
            "--file-selection"]
        if self.title:
            cmdline += ["--title", self.title]
        if self.multiple:
            cmdline += ["--multiple"]

        if self.mode == "save":
            cmdline += ["--save"]
        elif self.mode == "dir":
            cmdline += ["--directory"]
        if self.path:
            cmdline += ["--filename", self.path]
        if self.icon:
            cmdline += ["--icon", self.icon]

        # Checking if using mime pattern, and exists in dict # ['image','video']
        filters_exist = isinstance(self.filters, list) and len(self.filters)
        filter_str = self._build_zenity_filter_string(self.filters) if filters_exist else None

        # Use MIME-based filter if available Or else fallback to original
        if filter_str:
            cmdline += ["--file-filter", filter_str]
        elif filters_exist:
            for f in self.filters:
                if isinstance(f, str):
                    cmdline += ["--file-filter", f]
                else:
                    cmdline += [
                        "--file-filter",
                        "{name} | {flt}".format(name=f[0], flt=" ".join(f[1:]))
                    ]
        return cmdline

    def _build_zenity_filter_string(self, user_types):
        """
        For getting Zenity file filter with Readable Label

        :param user_types: List of logical file types like ["image", "pdf", "docx"]
        :return: Zenity filter string in the form "Label | *.ext *.ext" or None if no matching extensions
        """
        matching_extensions = set()
        filter_label = "Files"  # Default label if no type matches

        for file_type in user_types:
            mime_pattern = self.mime_type.get(file_type)
            if not mime_pattern:
                continue

            # When category like "image/", "text/", "video/" passed in
            if mime_pattern.endswith("/"):
                for ext, mapped_mime in mimetypes.types_map.items():
                    if mapped_mime.startswith(mime_pattern):
                        matching_extensions.add(ext)
                filter_label = file_type.capitalize()
            else:  # Exact MIME type like "application/pdf"
                matching_extensions.update(mimetypes.guess_all_extensions(mime_pattern))
                filter_label = file_type.capitalize()

        if not matching_extensions:
            return None

        # Zenity expects: "Label | *.ext *.ext ..."
        patterns = [f"*{ext.lstrip('.')}" for ext in sorted(matching_extensions)]
        return f"{filter_label} | {' '.join(patterns)}"


class KDialogFileChooser(SubprocessFileChooser):
    '''A FileChooser implementation using KDialog (on GNU/Linux).

    Not implemented features:
    * show_hidden
    * preview
    '''

    executable = "kdialog"
    separator = "\n"
    successretcode = 0

    def _gen_cmdline(self):
        cmdline = [which(self.executable)]

        filt = []
        for f in self.filters:
            if isinstance(f, str):
                filt += [f]
            else:
                filters = ''
                for ext in self.filters:
                    exts = ''
                    for y in ext[1:]:
                        exts += f' {y};'
                    x = f'{ext[0]} ({exts})|'
                    filters += x
                filt = [filters[:-1]]

        if self.mode == "dir":
            cmdline += [
                "--getexistingdirectory",
                (self.path if self.path else os.path.expanduser("~"))
            ]
        elif self.mode == "save":
            cmdline += [
                "--getsavefilename",
                (self.path if self.path else os.path.expanduser("~")),
                " ".join(filt)
            ]
        else:
            cmdline += [
                "--getopenfilename",
                (self.path if self.path else os.path.expanduser("~")),
                " ".join(filt)
            ]
        if self.multiple:
            cmdline += ["--multiple", "--separate-output"]
        if self.title:
            cmdline += ["--title", self.title]
        if self.icon:
            cmdline += ["--icon", self.icon]
        return cmdline


class YADFileChooser(SubprocessFileChooser):
    '''A NativeFileChooser implementation using YAD (on GNU/Linux).

    Not implemented features:
    * show_hidden
    '''

    executable = "yad"
    separator = "|?|"
    successretcode = 0

    def _gen_cmdline(self):
        cmdline = [
            which(self.executable),
            "--file",
            "--confirm-overwrite",
            "--geometry",
            "800x600+150+150"
        ]
        if self.multiple:
            cmdline += ["--multiple", "--separator", self.separator]
        if self.mode == "save":
            cmdline += ["--save"]
        elif self.mode == "dir":
            cmdline += ["--directory"]
        if self.preview:
            cmdline += ["--add-preview"]
        if self.path:
            cmdline += ["--filename", self.path]
        if self.title:
            cmdline += ["--name", self.title]
        if self.icon:
            cmdline += ["--window-icon", self.icon]
        for f in self.filters:
            if isinstance(f, str):
                cmdline += ["--file-filter", f]
            else:
                cmdline += [
                    "--file-filter",
                    "{name} | {flt}".format(name=f[0], flt=" ".join(f[1:]))
                ]
        return cmdline


CHOOSERS = {
    "gnome": ZenityFileChooser,
    "kde": KDialogFileChooser,
    "yad": YADFileChooser
}


class LinuxFileChooser(FileChooser):
    '''FileChooser implementation for GNu/Linux. Accepts one additional
    keyword argument, *desktop_override*, which, if set, overrides the
    back-end that will be used. Set it to "gnome" for Zenity, to "kde"
    for KDialog and to "yad" for YAD (Yet Another Dialog).
    If set to None or not set, a default one will be picked based on
    the running desktop environment and installed back-ends.
    '''

    desktop = None
    if (str(os.environ.get("XDG_CURRENT_DESKTOP")).lower() == "kde"
            and which("kdialog")):
        desktop = "kde"
    elif (str(os.environ.get("DESKTOP_SESSION")).lower() == "trinity"
            and which('kdialog')):
        desktop = "kde"
    elif which("yad"):
        desktop = "yad"
    elif which("zenity"):
        desktop = "gnome"

    def _file_selection_dialog(self, desktop_override=desktop, **kwargs):
        if not desktop_override:
            desktop_override = self.desktop
        # This means we couldn't find any back-end
        if not desktop_override:
            raise OSError("No back-end available. Please install one.")

        chooser = CHOOSERS[desktop_override]
        c = chooser(**kwargs)
        return c.run()


def instance():
    return LinuxFileChooser()
