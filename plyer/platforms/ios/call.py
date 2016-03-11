'''
IOS Call
----------
'''

from plyer.facades import Call
from pyobjus import autoclass, objc_str
from pyobjus.dylib_manager import load_framework

load_framework('/System/Library/Frameworks/UIKit.framework')

NSURL = autoclass('NSURL')
NSString = autoclass('NSString')
UIApplication = autoclass('UIApplication')


class IOSCall(Call):

    def _makecall(self, **kwargs):
        tel = kwargs.get('tel')
        url = NSURL("tel://" + tel);
        UIApplication.SharedApplication.OpenUrl(url);

    def _dialcall(self, **kwargs):
    	pass
        #Not possible, Access not provided by iPhone SDK

def instance():
    return IOSCall()
