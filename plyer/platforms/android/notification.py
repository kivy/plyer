from jnius import autoclass
from plyer.facades import Notification
from plyer.platforms.android import activity, SDK_INT
from android.broadcast import BroadcastReceiver

PythonActivity = autoclass('org.renpy.android.PythonActivity')
PendingIntent = autoclass('android.app.PendingIntent')
Intent = autoclass('android.content.Intent')
System = autoclass('java.lang.System')
AndroidString = autoclass('java.lang.String')
Context = autoclass('android.content.Context')
NotificationBuilder = autoclass('android.app.Notification$Builder')
Drawable = autoclass("{}.R$drawable".format(activity.getPackageName()))
PythonService = autoclass('org.renpy.android.PythonService')
if SDK_INT > 22:
    ActionBuilder = autoclass('android.app.Notification$Action$Builder')


class AndroidNotification(Notification):

    def _get_notification_service(self):
        if not hasattr(self, '_ns'):
            self._ns = activity.getSystemService(Context.NOTIFICATION_SERVICE)
        return self._ns

    def _notify(self, **kwargs):
        '''
        Generate Notification.
        '''
        try:
            request_id = int(System.curretTimeMillis())
            # get a requestid for pending indent
        except Exception as e:
            raise Exception('Unable to get id', str(e))

        service = PythonService.mService
        # python service
        intent = Intent(intent.ACTION_PROVIDER_CHANGED)
        # Broadcast Action

        icon = getattr(Drawable, kwargs.get('icon_android', 'icon'))
        noti = NotificationBuilder(activity)
        try:
            noti.setContentTitle(AndroidString(
                kwargs.get('title').encode('utf-8')))
            noti.setContentText(AndroidString(
                kwargs.get('message').encode('utf-8')))
            noti.setTicker(AndroidString(
                kwargs.get('ticker').encode('utf-8')))
            noti.setSmallIcon(icon)
            noti.setAutoCancel(True)
        except Exception as e:
            raise Exception('', str(e))

        if SDK_INT >= 16:
            for name, icon in kwargs['buttons'].items():
                pending_intent = PendingIntent.getBroadcast(service,
                                                            request_id,
                                                            intent,
                                                            0)
                if SDK_INT < 23:
                    noti.addAction(icon, AndroidString(name), pending_intent)

                else:
                    action = ActionBuilder(icon,
                                           AndroidString(name),
                                           pending_intent)
                    action = action.build()
                    noti.addAction(action)

        try:
            if SDK_INT >= 16:
                noti = noti.build()
            else:
                noti = noti.getNotification()

            self._get_notification_service().notify(0, noti)
        except Exception as e:
            raise Exception('', str(e))


def instance():
    return AndroidNotification()
