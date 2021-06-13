'''
Android Brightness
------------------
'''

from jnius import autoclass
from plyer.facades import Brightness
from plyer.platform.android import activity, require_permissions

System = autoclass('android.provider.Settings$System')


class AndroidBrightness(Brightness):

    def _current_level(self):

        System.putInt(
            activity.getContentResolver(),
            System.SCREEN_BRIGHTNESS_MODE,
            System.SCREEN_BRIGHTNESS_MODE_MANUAL)
        cr_level = System.getInt(
            mActivity.getContentResolver(),
            System.SCREEN_BRIGHTNESS)
        return (cr_level / 255.) * 100

    @require_permissions("WRITE_SETTINGS")
    def _set_level(self, level):
        System.putInt(
            mActivity.getContentResolver(),
            System.SCREEN_BRIGHTNESS,
            (level / 100.) * 255)


def instance():
    return AndroidBrightness()
