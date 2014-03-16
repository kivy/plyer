from jnius import autoclass, cast
from plyer.platforms.android import activity, api_level
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
            if api_level < 18:
                raise NotImplementedError(
                    'Android API level too low to use this feature')
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
            if api_level < 18:
                raise NotImplementedError(
                    'Android API level too low to use this feature')
            activity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_USER_PORTRAIT)
        else:
            activity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT)

    def _set_free(self, **kwargs):
        user = kwargs.get('user')
        full = kwargs.get('full')

        if user:
            if full:
                if api_level < 18:
                    raise NotImplementedError(
                        'Android API level too low to use this feature')
                activity.setRequestedOrientation(
                    ActivityInfo.SCREEN_ORIENTATION_FULL_USER)
            else:
                activity.setRequestedOrientation(
                    ActivityInfo.SCREEN_ORIENTATION_USER)
        else:
            if full:
                activity.setRequestedOrientation(
                    ActivityInfo.SCREEN_ORIENTATION_FULL_SENSOR)
            else:
                activity.setRequestedOrientation(
                    ActivityInfo.SCREEN_ORIENTATION_SENSOR)

    def _lock(self, **kwargs):
        activity.setRequestedOrientation(
            ActivityInfo.SCREEN_ORIENTATION_LOCKED)
            
        

def instance():
    return AndroidOrientation()
