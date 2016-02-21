from os.path import dirname
from os.path import join

from pyobjus import autoclass
from pyobjus.dylib_manager import load_dylib, make_dylib


def load_consts(name, frameworks=[]):
    make_dylib(join(dirname(__file__), name + '.m'),
               frameworks=['Foundation'] + frameworks)
    load_dylib(join(dirname(__file__), name + '.dylib'))
    objc_class = autoclass(name)

    class wrapper(object):
        def __getattr__(self, item):
            try:
                return object.__getattribute__(self, item)
            except AttributeError:
                return getattr(objc_class, 'get' + item)().cString()
    wrapper.__name__ = name
    return wrapper()


try:
    CBAdvertisementDataKeys = load_consts('CBAdvertisementDataKeys', ['CoreBluetooth'])
except Exception:
    class CBAdvertisementDataKeys(object):
        LocalName = 'kCBAdvDataLocalName'
        ServiceUUIDs = 'kCBAdvDataServiceUUIDs'
        ManufacturerData = 'kCBAdvDataManufacturerData'

