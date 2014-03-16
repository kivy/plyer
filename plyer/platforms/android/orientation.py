from jnius import autoclass, cast
from plyer.platforms.android import activity
from plyer.facades import Orientation

ActivityInfo = autoclass('android.content.pm.ActivityInfo')

class AndroidOrientation(Orientation):

    def _set_landscape(self, **kwargs):
        reverse = kwargs.get('reverse')
        sensor = kwargs.get('sensor')
        user = kwargs.get('user')

        if not sensor:
            if reverse:
                activity.setRequestedOrientation(
                    ActivityInfo.SCREEN_ORIENTATION_REVERSE_LANDSCAPE)
            else:
                activity.setRequestedOrientation(
                    ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE)
            return

        if user:
            activity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_USER_LANDSCAPE)
        else:
            activity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE)

    def _set_portrait(self, **kwargs):
        reverse = kwargs.get('reverse')
        sensor = kwargs.get('sensor')
        user = kwargs.get('user')

        if not sensor:
            if reverse:
                activity.setRequestedOrientation(
                    ActivityInfo.SCREEN_ORIENTATION_REVERSE_PORTRAIT)
            else:
                activity.setRequestedOrientation(
                    ActivityInfo.SCREEN_ORIENTATION_PORTRAIT)
            return

        if user:
            activity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_USER_PORTRAIT)
        else:
            activity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT)

    def _lock(self, **kwargs):
        activity.setRequestedOrientation(
            ActivityInfo.SCREEN_ORIENTATION_LOCKED)
            
        

def instance():
    return AndroidOrientation()
