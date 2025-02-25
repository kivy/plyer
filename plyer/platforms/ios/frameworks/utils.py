from plyer.platforms import ios
from os.path import join, dirname
from os import environ
from pyobjus.dylib_manager import load_framework


def load_plyer_framework(framework):
    framework_directory = join(dirname(ios.__file__), "frameworks")
    if 'SIMULATOR_DEVICE_NAME' in environ:
        path = join(framework_directory, "simulator", framework)
    else:
        path = join(framework_directory, framework)
    load_framework(path)
