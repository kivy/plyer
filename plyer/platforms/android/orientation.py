from jnius import autoclass
from plyer.platforms.android import activity
from plyer.facades import Orientation

ActivityInfo = autoclass('android.content.pm.ActivityInfo')
Surface = autoclass('android.view.Surface')


class AndroidOrientation(Orientation):

    def _set_landscape(self, **kwargs):
        reverse = kwargs.get('reverse')
        if reverse:
            activity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_REVERSE_LANDSCAPE)
        else:
            activity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE)

    def _set_portrait(self, **kwargs):
        reverse = kwargs.get('reverse')
        if reverse:
            activity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_REVERSE_PORTRAIT)
        else:
            activity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_PORTRAIT)

    def _set_sensor(self, **kwargs):
        mode = kwargs.get('mode')

        if mode == 'any':
            activity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_SENSOR)
        elif mode == 'landscape':
            activity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE)
        elif mode == 'portrait':
            activity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT)

    def _get_orientation(self):
        orientations = {
            Surface.ROTATION_0: 'portrait',
            Surface.ROTATION_90: 'landscape',
            Surface.ROTATION_180: 'portrait-reversed',
            Surface.ROTATION_270: 'landscape-reversed',
        }

        rotation = activity.getWindowManager().getDefaultDisplay().getRotation()

        return orientations.get(rotation, 'unknown')


def instance():
    return AndroidOrientation()
