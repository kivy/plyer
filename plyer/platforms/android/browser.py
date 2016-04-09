'''
Android Browser
-----------
'''

from jnius import autoclass
from plyer.facades import Browser
from plyer.platforms.android import activity

Intent = autoclass('android.content.Intent')
uri = autoclass('android.net.Uri')

class AndroidBrowser(Browser):
    def _open(self, **kwargs):
        intent = Intent(Intent.ACTION_VIEW)
        uri = kwargs.get('uri')
        intent.setData(uri.parse(uri))
        activity.startActivity(intent)

def instance():
    return AndroidBrowser()
