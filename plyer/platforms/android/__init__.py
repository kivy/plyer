from os import environ
from jnius import autoclass

ANDROID_VERSION = autoclass('android.os.Build$VERSION')
SDK_INT = ANDROID_VERSION.SDK_INT

if 'PYTHON_SERVICE_ARGUMENT' in environ:
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
    except Exception:
        PythonService = autoclass('org.renpy.android.PythonService')
    activity = PythonService.mService
else:
    try:
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
    except Exception:
        PythonActivity = autoclass('org.renpy.android.PythonActivity')
    activity = PythonActivity.mActivity
