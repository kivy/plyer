'''
Module of Android API for plyer.notification.
'''

from jnius import autoclass
from plyer.facades import Notification
from plyer.platforms.android import activity, SDK_INT

ANDROIDSTRING = autoclass('java.lang.String')
CONTEXT = autoclass('android.content.Context')
NOTIFICATIONBUILDER = autoclass('android.app.Notification$Builder')
DRAWABLE = autoclass("{}.R$drawable".format(activity.getPackageName()))


class AndroidNotification(Notification):
    # pylint: disable=too-few-public-methods
    '''
    Implementation of Android notification API.
    '''

    def __init__(self):
        self._ns = None

    def _get_notification_service(self):
        if not self._ns:
            self._ns = activity.getSystemService(
                CONTEXT.NOTIFICATION_SERVICE
            )
        return self._ns

    def _notify(self, **kwargs):
        icon = getattr(DRAWABLE, kwargs.get('icon_android', 'icon'))
        noti = NOTIFICATIONBUILDER(activity)
        noti.setContentTitle(ANDROIDSTRING(
            kwargs.get('title').encode('utf-8')))
        noti.setContentText(ANDROIDSTRING(
            kwargs.get('message').encode('utf-8')))
        noti.setTicker(ANDROIDSTRING(
            kwargs.get('ticker').encode('utf-8')))
        noti.setSmallIcon(icon)
        noti.setAutoCancel(True)

        if SDK_INT >= 16:
            noti = noti.build()
        else:
            noti = noti.getNotification()

        self._get_notification_service().notify(0, noti)


def instance():
    '''
    Instance for facade proxy.
    '''
    return AndroidNotification()
