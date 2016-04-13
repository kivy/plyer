from os import environ
from jnius import autoclass

__all__ = ['PythonService', 'PythonActivity', 'activity',
           'ANDROID_VERSION', 'SDK_INT', 'USE_SDL2']

# Determine whether SDL2 is used. if so, use PythonActivity provided by kivy
try:
    from kivy.setupconfig import USE_SDL2
except ImportError:
    USE_SDL2 = False

if USE_SDL2:
    clsname = 'org.kivy.android.PythonActivity'
else:
    clsname = 'org.renpy.android.PythonActivity'


ANDROID_VERSION = autoclass('android.os.Build$VERSION')
SDK_INT = ANDROID_VERSION.SDK_INT

if 'PYTHON_SERVICE_ARGUMENT' in environ:
    PythonService = autoclass(clsname)
    activity = PythonService.mService
else:
    PythonActivity = autoclass(clsname)
    activity = PythonActivity.mActivity

