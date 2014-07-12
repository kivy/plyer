from jnius import autoclass, cast
from plyer.platforms.android import activity
from plyer.facades import UniqueID

TelephonyManager = autoclass('android.telephony.TelephonyManager')
Context = autoclass('android.content.Context')


class AndroidUniqueID(UniqueID):

    def _get_uid(self):
        manager = cast('android.telephony.TelephonyManager',
            activity.getSystemService(Context.TELEPHONY_SERVICE))
        return manager.getDeviceId()


def instance():
    return AndroidUniqueID()
