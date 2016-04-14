from jnius import autoclass
from . import activity
from plyer.facades import UniqueID

Secure = autoclass('android.provider.Settings$Secure')


class AndroidUniqueID(UniqueID):

    def _get_uid(self):
        return Secure.getString(activity.getContentResolver(),
                                Secure.ANDROID_ID)


def instance():
    return AndroidUniqueID()
