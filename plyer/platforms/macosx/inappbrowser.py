
from plyer.facades.inappbrowser import InAppBrowser
import webbrowser


class MacosxBrowser():

    def _open_url(self, **kwargs):
        try:
            url = kwargs.get('url', '')
            if not url:
                raise ValueError('empty url provided!')
        except ValueError as e:
            url = "https://kivy.org/#home"
            print(e)
        webbrowser.open(url)


def instance():
    return MacosxBrowser()
