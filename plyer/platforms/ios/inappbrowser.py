try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

from plyer.facades import InAppBrowser
from pyobjus import autoclass, objc_str
from pyobjus.dylib_manager import load_framework

# load_framework('/System/Library/Frameworks/UIKit.framework')

NSURL = autoclass('NSURL')
NSString = autoclass('NSString')
UIApplication = autoclass('UIApplication')


class iOSInAppBrowser(InAppBrowser):
    def _open_url(self, **kwargs):
        url = kwargs.get('url', '')

        nsurl = NSURL.alloc().initWithString_(objc_str(str(url)))

        UIApplication.sharedApplication().openURL_(nsurl)


def instance():
    return iOSInAppBrowser()
