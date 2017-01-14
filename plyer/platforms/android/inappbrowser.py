from jnius import cast
from jnius import autoclass
from plyer.facades import InAppBrowser

PythonActivity = autoclass('org.kivy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
Uri = autoclass('android.net.Uri')


class AndroidInAppBrowser():

    def _access_url(self, **kwargs):
        uri = kwargs.get('url', '')

        intent = Intent()
        intent.setAction(Intent.ACTION_VIEW)
        intent.setData(Uri.parse(uri))

        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        currentActivity.startActivity(intent)


def instance():
    return AndroidTnAppBrowser()
