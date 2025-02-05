from importlib.resources import path

from plyer.facades import Keystore
from pyobjus import autoclass, objc_str
from pyobjus.dylib_manager import load_framework


class IosKeystore(Keystore):
    """
    In order to get this to work, I had to write an Objective-C class that contains the functions to interact with the
    keychain. They were a part of a framework, and not a class, and are thus, unable to be accessed with pyobjus
    normally. I compiled it into a .framework to comply with Apple's App Store guidelines. This will give you a bridge from Objective-C to Python that will allow you to interact with the keychain.

    It comes with three functions, you can see usage examples in the class below:
    - (BOOL)saveWithService:(NSString *)service account:(NSString *)account value:(NSString *)value;
    - (NSString *)retrieveWithService:(NSString *)service account:(NSString *)account;
    - (BOOL)deleteWithService:(NSString *)service account:(NSString *)account;
    """

    @staticmethod
    def KeychainBridge():
        with path('plyer.tools', 'KeychainBridge.framework') as framework_path:
            load_framework(str(framework_path))
            return autoclass('KeychainBridge')

    def _set_key(self, servicename, key, value, *args, **kwargs):
        keychain_bridge = self.KeychainBridge()
        keychain_bridge.deleteWithService_account_(
            objc_str(servicename), objc_str(key)
        )
        return keychain_bridge.saveWithService_account_value_(objc_str(servicename), objc_str(key),
                                                              objc_str(value))

    def _get_key(self, servicename, key, *args, **kwargs):
        keychain_bridge = self.KeychainBridge()
        if result := keychain_bridge.retrieveWithService_account_(
                objc_str(servicename), objc_str(key)
        ):
            result = result.UTF8String()
            """
            for some reason, the ios-sim returns a bytes object, but the actual phone returns a str object that you 
            can't use isinstance on
            """
            if 'bytes' in str(type(result)):
                result = result.decode('utf-8')
            return result
        return None


def instance():
    return IosKeystore()
