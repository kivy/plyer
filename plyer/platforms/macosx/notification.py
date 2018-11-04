'''
Module of MacOS API for plyer.notification.
'''

from plyer.facades import Notification

try:
    import pyobjus  # pylint: disable=unused-import
except ImportError:
    raise Exception(
        "pyobjus missing, please install it. "
        "`python -m pip install git+http://github.com/kivy/pyobjus/`"
    )

from pyobjus import (  # pylint: disable=import-error
    autoclass, protocol, objc_str, ObjcBOOL
)
from pyobjus.dylib_manager import (  # pylint: disable=import-error
    load_framework, INCLUDE
)

load_framework(INCLUDE.AppKit)
load_framework(INCLUDE.Foundation)

NSUserNotification = autoclass('NSUserNotification')
NSUserNotificationCenter = autoclass('NSUserNotificationCenter')


class OSXNotification(Notification):
    '''
    Implementation of MacOS notification API.
    '''

    def _notify(self, **kwargs):
        title = kwargs.get('title', '')
        message = kwargs.get('message', '')
        app_name = kwargs.get('app_name', '')
        # app_icon, timeout, ticker are not supported (yet)

        notification = NSUserNotification.alloc().init()
        notification.setTitle_(objc_str(title))
        notification.setSubtitle_(objc_str(app_name))
        notification.setInformativeText_(objc_str(message))

        usrnotifctr = NSUserNotificationCenter.defaultUserNotificationCenter()
        usrnotifctr.setDelegate_(self)
        usrnotifctr.deliverNotification_(notification)

    @protocol('NSUserNotificationCenterDelegate')
    def userNotificationCenter_shouldPresentNotification_(
            self, center, notification):
        # pylint: disable=invalid-name,missing-docstring
        # pylint: disable=unused-argument,no-self-use
        return ObjcBOOL(True)


def instance():
    '''
    Instance for facade proxy.
    '''
    return OSXNotification()
