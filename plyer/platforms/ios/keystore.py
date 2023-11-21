from importlib.resources import path

from plyer.facades import Keystore
from pyobjus import autoclass, objc_str
from pyobjus.dylib_manager import load_dylib


class IosKeystore(Keystore):
    """
    In order to get this to work, I had to write an Objective-C class that contains the functions to interact with the
    keychain. They were a part of a framework, and not a class, and are thus, unable to be accessed with pyobjus
    normally. If for some reason you want to do this yourself, the original file (KeychainBridge.m) is in the 'tools'
    directory. You can compile it yourself using the following commands(macOS):

    First compile the ios-sim dylib:
    clang -target x86_64-apple-ios13.0-simulator -isysroot $(xcrun --sdk iphonesimulator --show-sdk-path) \
    -F$(xcrun --sdk iphonesimulator --show-sdk-path)/System/Library/Frameworks -framework Security -framework Foundation \
    -shared -o KeychainBridge_sim.dylib KeychainBridge.m


    Then compile the ios dylib:
    clang -target arm64-apple-ios13.0 -isysroot $(xcrun --sdk iphoneos --show-sdk-path) -F$(xcrun --sdk iphoneos \
    --show-sdk-path)/System/Library/Frameworks -framework Security -framework Foundation -shared -o \
    KeychainBridge_device.dylib KeychainBridge.m

    then run this command to create a fat dylib:
    lipo -create -output KeychainBridge.dylib KeychainBridge_sim.dylib KeychainBridge_device.dylib

    This will give you a bridge from Objective-C to Python that will allow you to interact with the keychain,
    this will work on both the Xcode iOS simulator (x86_64) and an iPhone (arm64). If you only want one or the other,
    you can just use the sim or device dylib and ignore the other two commands.

    It comes with three functions, you can see usage examples in the class below:
    - (BOOL)saveWithService:(NSString *)service account:(NSString *)account value:(NSString *)value;
    - (NSString *)retrieveWithService:(NSString *)service account:(NSString *)account;
    - (BOOL)deleteWithService:(NSString *)service account:(NSString *)account;
    """

    @staticmethod
    def KeychainBridge():
        with path('plyer.tools.KeychainBridge', 'KeychainBridge.dylib') as dylib_path:
            load_dylib(str(dylib_path))
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
