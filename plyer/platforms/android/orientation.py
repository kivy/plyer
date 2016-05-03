from jnius import autoclass, cast
from plyer.platforms.android import activity
from plyer.facades import Orientation

ActivityInfo = autoclass('android.content.pm.ActivityInfo')
Configuration = autoclass('android.content.res.Configuration')
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
        screenOrientation = activity.getResources().getConfiguration().orientation
        surfaceRotation = activity.getWindowManager().getDefaultDisplay().getRotation()
        
        if surfaceRotation == Surface.ROTATION_0 or surfaceRotation == Surface.ROTATION_90:
	        if screenOrientation == Configuration.ORIENTATION_PORTRAIT:
		        return ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
	        elif screenOrientation == Configuration.ORIENTATION_LANDSCAPE:
		        return ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
        elif surfaceRotation == Surface.ROTATION_180 or surfaceRotation == Surface.ROTATION_270:
	        if screenOrientation == Configuration.ORIENTATION_PORTRAIT:
		        return ActivityInfo.SCREEN_ORIENTATION_REVERSE_PORTRAIT
	        elif screenOrientation == Configuration.ORIENTATION_LANDSCAPE:
		        return ActivityInfo.SCREEN_ORIENTATION_REVERSE_LANDSCAPE
		        
def instance():
    return AndroidOrientation()
