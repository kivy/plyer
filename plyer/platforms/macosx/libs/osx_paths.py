import ctypes
import os


def NSIterateSearchPaths(directory):
    CoreFoundation = ctypes.cdll.LoadLibrary("/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation")
    NSStartSearchPathEnumeration = CoreFoundation.NSStartSearchPathEnumeration
    NSGetNextSearchPathEnumeration = CoreFoundation.NSGetNextSearchPathEnumeration
    PATH_MAX = os.pathconf('/', os.pathconf_names['PC_PATH_MAX'])
    PATH_ENCODING = 'utf8'
    path_buffer = ctypes.create_string_buffer(PATH_MAX)
    paths = []
    state = NSStartSearchPathEnumeration(directory, 1)
    while True:
        state = NSGetNextSearchPathEnumeration(state, path_buffer)
        if state == 0:
            break
        path = os.path.expanduser(path_buffer.value.decode(PATH_ENCODING))
        return path