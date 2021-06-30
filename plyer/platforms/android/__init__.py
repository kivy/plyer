from os import environ
from logging import getLogger

from functools import wraps
from jnius import autoclass

ANDROID_VERSION = autoclass('android.os.Build$VERSION')
SDK_INT = ANDROID_VERSION.SDK_INT
LOG = getLogger(__name__)


try:
    from android import config
    ns = config.JAVA_NAMESPACE
except (ImportError, AttributeError):
    ns = 'org.renpy.android'


if 'PYTHON_SERVICE_ARGUMENT' in environ:
    PythonService = autoclass(ns + '.PythonService')
    activity = PythonService.mService
else:
    PythonActivity = autoclass(ns + '.PythonActivity')
    activity = PythonActivity.mActivity


def resolve_permission(permission):
    """Helper method to allow passing a permission by name
    """
    from android.permissions import Permission
    if hasattr(Permission, permission):
        return getattr(Permission, permission)
    return permission


def require_permissions(*permissions, handle_denied=None):
    """
    A decorator for android plyer functions allowing to automatically request
    necessary permissions when a method is called.

    usage:
    @require_permissions(Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION)
    def start_gps(...):
        ...


    if the permissions haven't been granted yet, the require_permissions method
    will be called first, and the actual method will be set as a callback to
    execute when the user accept or refuse permissions, if you want to handle
    the cases where some of the permissions are denied, you can set a callback
    method to `handle_denied`. When set, and if some permissions are refused
    this function will be called with the list of permissions that were refused
    as a parameter. If you don't set such a handler, the decorated method will
    be called in all the cases.
    """

    def decorator(function):
        LOG.debug(f"decorating function {function.__name__}")
        @wraps(function)
        def wrapper(*args, **kwargs):
            nonlocal permissions
            from android.permissions import request_permissions, check_permission

            def callback(permissions, grant_results):
                LOG.debug(f"callback called with {dict(zip(permissions, grant_results))}")
                if handle_denied and not all(grant_results):
                    handle_denied([
                        permission
                        for (granted, permission) in zip(grant_results, permissions)
                        if granted
                    ])
                else:
                    function(*args, **kwargs)

            permissions = [resolve_permission(permission) for permission in permissions]
            permissions = [
                permission
                for permission in permissions
                if not check_permission(permission)
            ]
            LOG.debug(f"needed permissions: {permissions}")

            if permissions:
                LOG.debug("calling request_permissions with callback")
                request_permissions(permissions, callback)
            else:
                LOG.debug("no missing permissiong calling function directly")
                function(*args, **kwargs)

        return wrapper
    return decorator
