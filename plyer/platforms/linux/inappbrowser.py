
from plyer.facades.inappbrowser import InAppBrowser
import webbrowser


class LinuxAppBrowser():

    def _open_url(self, **kwargs):
        url = kwargs.get('url', '')
        webbrowser.open(url)


def instance():
    return LinuxAppBrowser()
