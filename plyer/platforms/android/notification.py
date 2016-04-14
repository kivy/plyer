from jnius import autoclass
from plyer.facades import Notification
from . import activity, SDK_INT

AndroidString = autoclass('java.lang.String')
Context = autoclass('android.content.Context')
NotificationBuilder = autoclass('android.app.Notification$Builder')
Drawable = autoclass("{}.R$drawable".format(activity.getPackageName()))


class AndroidNotification(Notification):
    def _get_notification_service(self):
        if not hasattr(self, '_ns'):
            self._ns = activity.getSystemService(Context.NOTIFICATION_SERVICE)
        return self._ns

    def _notify(self, **kwargs):
        icon = getattr(Drawable, kwargs.get('icon_android', 'icon'))
        noti = NotificationBuilder(activity)
        noti.setContentTitle(AndroidString(
            kwargs.get('title').encode('utf-8')))
        noti.setContentText(AndroidString(
            kwargs.get('message').encode('utf-8')))
        noti.setTicker(AndroidString(
            kwargs.get('ticker').encode('utf-8')))
        noti.setSmallIcon(icon)
        noti.setAutoCancel(True)

        if SDK_INT >= 16:
            noti = noti.build()
        else:
            noti = noti.getNotification()

        self._get_notification_service().notify(0, noti)


def instance():
    return AndroidNotification()
