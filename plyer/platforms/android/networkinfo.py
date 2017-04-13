'''
Android Network Information
---------------------------
'''

from plyer.facades import NetworkInfo
from jnius import autoclass, cast
from plyer.platforms.android import activity

Context = autoclass('android.content.Context')


class AndroidNetworkInfo(NetworkInfo):

    def __init__(self, **kwargs):
        super(AndroidNetworkInfo, self).__init__(**kwargs)
        self.ConnectivityManager = cast('android.net.ConnectivityManager',
            activity.getSystemService(Context.CONNECTIVITY_SERVICE))
        self.netinfo = self.ConnectivityManager.getActiveNetworkInfo()

    def _get_extra_info(self):
        return self.netinfo.getExtraInfo()

    def _get_subtype_name(self):
        return self.netinfo.getSubtypeName()

    def _get_type_name(self):
        return self.netinfo.getTypeName()

    def _is_available(self):
        return self.netinfo.isAvailable()

    def _is_connected(self):
        return self.netinfo.isConnected()

    def _is_roaming(self):
        return self.netinfo.isRoaming()


def instance():
    return AndroidNetworkInfo()
