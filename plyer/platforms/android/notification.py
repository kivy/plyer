from jnius import autoclass
from plyer.facades import Notification
from plyer.platforms.android import activity, SDK_INT

PythonActivity = autoclass('org.renpy.android.PythonActivity')
PendingIntent = autoclass('android.app.PendingIntent')
Intent = autoclass('android.content.Intent')
System = autoclass('java.lang.System')
RingtoneManager = autoclass('android.media.RingtoneManager')
AndroidString = autoclass('java.lang.String')
StackBuilder = autoclass('android.app.TaskStackBuilder')
Context = autoclass('android.content.Context')
NotificationBuilder = autoclass('android.app.Notification$Builder')
Drawable = autoclass("{}.R$drawable".format(activity.getPackageName()))


class AndroidNotification(Notification):
    def _get_notification_service(self):
        if not hasattr(self, '_ns'):
            self._ns = activity.getSystemService(Context.NOTIFICATION_SERVICE)
        return self._ns

    def _notify(self, **kwargs):

        request_id = int(System.curretTimeMillis())

        self.j_context = context = PythonActivity.mActivity

        stack_builder = StackBuilder.create(context)
        stack_builder.addParentStack(activity.class)

        ring_tone = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)

        result_intent = Intent(context, context.getClass()).addFlags(
                Intent.FLAG_ACTIVITY_SINGLE_TOP | Intent.FLAG_ACTIVITY_CLEAR_TOP)

        stack_builder.addNextIntent(result_intent)

        self._pending_intent = PendingIntent.getActivity(
            context, request_id,
            result_intent, PendingIntent.FLAG_UPDATE_CURRENT)

        self.lol = stack_builder.getPendingIntent(0, PendingIntent.FLAG_UPDATE_CURRENT)

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
        noti.sound = ring_tone
        noti.setContentIntent(self._pending_intent)


        if SDK_INT >= 16:
            noti = noti.build()
        else:
            noti = noti.getNotification()

        self._get_notification_service().notify(0, noti)


def instance():
    return AndroidNotification()
