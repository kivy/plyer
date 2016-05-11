__all__ = ('get_SystemMetrics')


import ctypes
from plyer.platforms.win.libs import win_api_defs


def get_SystemMetrics(val):
    mat = win_api_defs.GetSystemMetrics(val)
    return mat
