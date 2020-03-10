'''
Module of Android API for plyer.notification.

.. versionadded:: 1.0.0

.. versionchanged:: 1.4.0
    Fixed notifications not displaying due to missing NotificationChannel
    required by Android Oreo 8.0+ (API 26+).

.. versionchanged:: 1.4.0
    Added simple toaster notification.

.. versionchanged:: 1.4.0
    Fixed notifications not displaying big icons properly.
    Added option for custom big icon via `icon`.
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
NotificationManager = autoclass('android.app.NotificationManager')
Drawable = autoclass("{}.R$drawable".format(activity.getPackageName()))
PendingIntent = autoclass('android.app.PendingIntent')
Intent = autoclass('android.content.Intent')
Toast = autoclass('android.widget.Toast')
BitmapFactory = autoclass('android.graphics.BitmapFactory')


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
            self._ns = cast(NotificationManager, activity.getSystemService(
                Context.NOTIFICATION_SERVICE
            ))
        return self._ns

    def _build_notification_channel(self, name):
        '''
        Create a NotificationChannel using channel id of the application
        package name (com.xyz, org.xyz, ...) and channel name same as the
        provided notification title if the API is high enough, otherwise
        do nothing.

        .. versionadded:: 1.4.0
        '''

        if SDK_INT < 26:
            return

        channel = autoclass('android.app.NotificationChannel')

        app_channel = channel(
            self._channel_id, name, NotificationManager.IMPORTANCE_DEFAULT
        )
        self._get_notification_service().createNotificationChannel(
            app_channel
        )
        return app_channel

    @run_on_ui_thread
    def _toast(self, message):
        '''
        Display a popup-like small notification at the bottom of the screen.

        .. versionadded:: 1.4.0
        '''
        Toast.makeText(
            activity,
            cast('java.lang.CharSequence', AndroidString(message)),
            Toast.LENGTH_LONG
        ).show()

    @staticmethod
    def _set_icons(notification, icon=None):
        '''
        Set the small application icon displayed at the top panel together with
        WiFi, battery percentage and time and the big optional icon (preferably
        PNG format with transparent parts) displayed directly in the
        notification body.

        .. versionadded:: 1.4.0
        '''
        app_icon = Drawable.icon
        notification.setSmallIcon(app_icon)

        bitmap_icon = app_icon
        if icon is not None:
            bitmap_icon = BitmapFactory.decodeFile(icon)
            notification.setLargeIcon(bitmap_icon)
        elif icon == '':
            # we don't want the big icon set,
            # only the small one in the top panel
            pass
        else:
            bitmap_icon = BitmapFactory.decodeResource(
                python_act.getResources(), app_icon
            )
            notification.setLargeIcon(bitmap_icon)

    def _build_notification(self, title):
        '''
        .. versionadded:: 1.4.0
        '''
        if SDK_INT < 26:
            noti = NotificationBuilder(activity)
        else:
            self._channel = self._build_notification_channel(title)
            noti = NotificationBuilder(activity, self._channel_id)
        return noti

    @staticmethod
    def _set_open_behavior(notification):
        '''
        Open the source application when user opens the notification.

        .. versionadded:: 1.4.0
        '''

        # create Intent that navigates back to the application
        app_context = activity.getApplication().getApplicationContext()
        notification_intent = Intent(app_context, python_act)

        # set flags to run our application Activity
        notification_intent.setFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP)
        notification_intent.setAction(Intent.ACTION_MAIN)
        notification_intent.addCategory(Intent.CATEGORY_LAUNCHER)

        # get our application Activity
        pending_intent = PendingIntent.getActivity(
            app_context, 0, notification_intent, 0
        )

        notification.setContentIntent(pending_intent)
        notification.setAutoCancel(True)

    def _open_notification(self, notification):
        if SDK_INT >= 16:
            notification = notification.build()
        else:
            notification = notification.getNotification()

        self._get_notification_service().notify(0, notification)

    def _notify(self, **kwargs):
        noti = None
        message = kwargs.get('message').encode('utf-8')
        ticker = kwargs.get('ticker').encode('utf-8')
        title = AndroidString(
            kwargs.get('title', '').encode('utf-8')
        )
        icon = kwargs.get('app_icon')

        # decide whether toast only or proper notification
        if kwargs.get('toast'):
            self._toast(message)
            return
        else:
            noti = self._build_notification(title)

        # set basic properties for notification
        noti.setContentTitle(title)
        noti.setContentText(AndroidString(message))
        noti.setTicker(AndroidString(ticker))

        # set additional flags for notification
        self._set_icons(noti, icon=icon)
        self._set_open_behavior(noti)

        # launch
        self._open_notification(noti)


def instance():
    '''
    Instance for facade proxy.
    '''
    return AndroidNotification()
