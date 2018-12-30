'''
Module of Android API for plyer.notification.

.. versionadded:: 1.0.0

.. versionchanged:: 1.3.3
    Fixed notifications not displaying due to missing NotificationChannel
    required by Android Oreo 8.0+ (API 26+).

.. versionchanged:: 1.3.3
    Added simple toaster notification.
'''

from __future__ import unicode_literals
from android import python_act
from android.runnable import run_on_ui_thread
from jnius import autoclass, cast

from plyer.facades import Notification
from plyer.platforms.android import activity, SDK_INT

AndroidString = autoclass('java.lang.String')
Context = autoclass('android.content.Context')
NotificationBuilder = autoclass('android.app.Notification$Builder')
Drawable = autoclass("{}.R$drawable".format(activity.getPackageName()))
PendingIntent = autoclass('android.app.PendingIntent')
Intent = autoclass('android.content.Intent')
Toast = autoclass('android.widget.Toast')


class AndroidNotification(Notification):
    # pylint: disable=too-few-public-methods
    '''
    Implementation of Android notification API.

    .. versionadded:: 1.0.0
    '''

    def __init__(self):
        self._ns = None
        self._channel_id = activity.getPackageName()

    def _get_notification_service(self):
        if not self._ns:
            self._ns = activity.getSystemService(
                Context.NOTIFICATION_SERVICE
            )
        return self._ns

    def _build_notification_channel(self, name):
        '''
        Create a NotificationChannel using channel id of the application
        package name (com.xyz, org.xyz, ...) and channel name same as the
        provided notification title if the API is high enough, otherwise
        do nothing.

        .. versionadded:: 1.3.3
        '''

        if SDK_INT < 26:
            return

        manager = autoclass('android.app.NotificationManager')
        channel = autoclass('android.app.NotificationChannel')

        app_channel = channel(
            self._channel_id, name, manager.IMPORTANCE_DEFAULT
        )
        activity.getSystemService(manager).createNotificationChannel(
            app_channel
        )
        return app_channel

    @run_on_ui_thread
    def _toast(self, message):
        '''
        Display a popup-like small notification at the bottom of the screen.

        .. versionadded:: 1.3.3
        '''
        Toast.makeText(
            activity,
            cast('java.lang.CharSequence', AndroidString(message)),
            Toast.LENGTH_LONG
        ).show()

    def _notify(self, **kwargs):
        icon = getattr(Drawable, kwargs.get('icon_android', 'icon'))
        title = AndroidString(
            kwargs.get('title', '').encode('utf-8')
        )
        message = kwargs.get('message').encode('utf-8')

        # decide whether toast only or proper notification
        if kwargs.get('toast'):
            self._toast(message)
            return

        if SDK_INT < 26:
            noti = NotificationBuilder(activity)
        else:
            self._channel = self._build_notification_channel(title)
            noti = NotificationBuilder(activity, self._channel_id)

        noti.setContentTitle(title)
        noti.setContentText(AndroidString(message))
        noti.setTicker(AndroidString(
            kwargs.get('ticker').encode('utf-8')))
        noti.setSmallIcon(icon)
        noti.setAutoCancel(True)

        # clicking the notification will open the application
        app_context = activity.getApplication().getApplicationContext()
        notification_intent = Intent(app_context, python_act)

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
