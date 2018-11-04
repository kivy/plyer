'''
Module of Android API for plyer.notification.
'''

from android.config import JAVA_NAMESPACE
from jnius import autoclass
from plyer.facades import Notification
from plyer.platforms.android import activity, SDK_INT

AndroidString = autoclass('java.lang.String')
Context = autoclass('android.content.Context')
NotificationBuilder = autoclass('android.app.Notification$Builder')
Drawable = autoclass("{}.R$drawable".format(activity.getPackageName()))
PythonActivity = autoclass('{}.PythonActivity'.format(JAVA_NAMESPACE))
PendingIntent = autoclass('android.app.PendingIntent')
Intent = autoclass('android.content.Intent')


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
                Context.NOTIFICATION_SERVICE
            )
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

        # clicking the notification will open the application
        app_context = activity.getApplication().getApplicationContext()
        notification_intent = Intent(app_context, PythonActivity)
        notification_intent.setFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP)
        notification_intent.setAction(Intent.ACTION_MAIN)
        notification_intent.addCategory(Intent.CATEGORY_LAUNCHER)
        pending_intent = PendingIntent.getActivity(
            app_context, 0, notification_intent, 0
        )
        noti.setContentIntent(pending_intent)

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
