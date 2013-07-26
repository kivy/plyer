'''
Utils
=====

'''

__all__ = ('platform', )

from os import environ
from os import path
from sys import platform as _sys_platform

_platform_ios = None
_platform_android = None

def _determine_platform():
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

#: Return the version of the current platform, one of win, linux, android,
#: macosx, ios, unknown
platform = _determine_platform()


class Proxy(object):
    # taken from http://code.activestate.com/recipes/496741-object-proxying/

    __slots__ = ['_obj', '_name', '_facade']

    def __init__(self, name, facade):
        object.__init__(self)
        object.__setattr__(self, '_obj', None)
        object.__setattr__(self, '_name', name)
        object.__setattr__(self, '_facade', facade)

    def _ensure_obj(self):
        obj = object.__getattribute__(self, '_obj')
        if obj:
            return obj
        # do the import
        try:
            name = object.__getattribute__(self, '_name')
            module = 'plyer.platforms.{}.{}'.format(
                platform, name)
            mod = __import__(module, fromlist='.')
            obj = mod.instance()
        except:
            import traceback; traceback.print_exc()
            facade = object.__getattribute__(self, '_facade')
            obj = facade()

        object.__setattr__(self, '_obj', obj)
        return obj

    def __getattribute__(self, name):
        if name == '__doc__':
            return
        object.__getattribute__(self, '_ensure_obj')()
        return getattr(object.__getattribute__(self, '_obj'), name)

    def __delattr__(self, name):
        object.__getattribute__(self, '_ensure_obj')()
        delattr(object.__getattribute__(self, '_obj'), name)

    def __setattr__(self, name, value):
        object.__getattribute__(self, '_ensure_obj')()
        setattr(object.__getattribute__(self, '_obj'), name, value)

    def __bool__(self):
        object.__getattribute__(self, '_ensure_obj')()
        return bool(object.__getattribute__(self, '_obj'))

    def __str__(self):
        object.__getattribute__(self, '_ensure_obj')()
        return str(object.__getattribute__(self, '_obj'))

    def __repr__(self):
        object.__getattribute__(self, '_ensure_obj')()
        return repr(object.__getattribute__(self, '_obj'))


def whereis_exe(program):
    ''' Tries to find the program on the system path.
        Returns the path if it is found or None if it's not found.
    '''
    for p in environ.get('PATH', '').split(':'):
        if path.exists(path.join(p, program)) and \
            not path.isdir(path.join(p, program)):
            return path.join(p, program)
    return None
