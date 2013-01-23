from os import environ
from sys import platform as _sys_platform

_platform_ios = None
_platform_android = None


def platform():
    '''Return the version of the current platform.
    This will return one of: win, linux, android, macosx, ios, unknown

    .. versionadded:: 1.0.8

    .. warning:: ios is not currently reported.
    '''
    global _platform_ios, _platform_android

    if _platform_android is None:
        # ANDROID_ARGUMENT and ANDROID_PRIVATE are 2 environment variables from
        # python-for-android project
        _platform_android = 'ANDROID_ARGUMENT' in environ

    if _platform_ios is None:
        _platform_ios = (environ.get('KIVY_BUILD', '') == 'ios')

    # On android, _sys_platform return 'linux2', so prefer to check the import
    # of Android module than trying to rely on _sys_platform.
    if _platform_android is True:
        return 'android'
    elif _platform_ios is True:
        return 'ios'
    elif _sys_platform in ('win32', 'cygwin'):
        return 'win'
    elif _sys_platform in ('darwin', ):
        return 'macosx'
    elif _sys_platform in ('linux2', 'linux3'):
        return 'linux'
    return 'unknown'
