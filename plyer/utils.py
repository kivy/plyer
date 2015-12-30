'''
Utils
=====

'''

__all__ = ('platform', 'reify')

from os import environ
from os import path
from sys import platform as _sys_platform


class Platform(object):
    # refactored to class to allow module function to be replaced
    # with module variable

    def __init__(self):
        self._platform_ios = None
        self._platform_android = None

    def __eq__(self, other):
        return other == self._get_platform()

    def __ne__(self, other):
        return other != self._get_platform()

    def __str__(self):
        return self._get_platform()

    def __repr__(self):
        return 'platform name: \'{platform}\' from: \n{instance}'.format(
            platform=self._get_platform(),
            instance=super(Platform, self).__repr__()
        )

    def __hash__(self):
        return self._get_platform().__hash__()

    def _get_platform(self):

        if self._platform_android is None:
            # ANDROID_ARGUMENT and ANDROID_PRIVATE are 2 environment variables
            # from python-for-android project
            self._platform_android = 'ANDROID_ARGUMENT' in environ

        if self._platform_ios is None:
            self._platform_ios = (environ.get('KIVY_BUILD', '') == 'ios')

        # On android, _sys_platform return 'linux2', so prefer to check the
        # import of Android module than trying to rely on _sys_platform.
        if self._platform_android is True:
            return 'android'
        elif self._platform_ios is True:
            return 'ios'
        elif _sys_platform in ('win32', 'cygwin'):
            return 'win'
        elif _sys_platform == 'darwin':
            return 'macosx'
        elif _sys_platform[:5] == 'linux':
            return 'linux'
        return 'unknown'


platform = Platform()


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
            import traceback
            traceback.print_exc()
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
    path_split = ';' if platform == 'win' else ':'
    for p in environ.get('PATH', '').split(path_split):
        if path.exists(path.join(p, program)) and \
            not path.isdir(path.join(p, program)):
            return path.join(p, program)
    return None


class reify(object):
    '''
    Put the result of a method which uses this (non-data) descriptor decorator
    in the instance dict after the first call, effectively replacing the
    decorator with an instance variable.

    It acts like @property, except that the function is only ever called once;
    after that, the value is cached as a regular attribute. This gives you lazy
    attribute creation on objects that are meant to be immutable.

    Taken from the `Pyramid project <https://pypi.python.org/pypi/pyramid/>`_.

    To use this as a decorator::

         @reify
         def lazy(self):
              ...
              return hard_to_compute_int
         first_time = self.lazy   # lazy is reify obj, reify.__get__() runs
         second_time = self.lazy  # lazy is hard_to_compute_int
    '''

    def __init__(self, func):
        self.func = func
        self.__doc__ = func.__doc__

    def __get__(self, inst, cls):
        if inst is None:
            return self
        retval = self.func(inst)
        setattr(inst, self.func.__name__, retval)
        return retval
