from plyer.facades import Notification
import Foundation
import objc
import AppKit

class OSXNotification(Notification):
    def _notify(self, **kwargs):
        NSUserNotification = objc.lookUpClass('NSUserNotification')
        NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')
        notification = NSUserNotification.alloc().init()
        notification.setTitle_(kwargs.get('title').encode('utf-8'))
        #notification.setSubtitle_(str(subtitle))
        notification.setInformativeText_(kwargs.get('message').encode('utf-8'))
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
        #notification.setHasActionButton_(False)
        #notification.setOtherButtonTitle_("View")
        #notification.setUserInfo_({"action":"open_url", "value":url})
        NSUserNotificationCenter.defaultUserNotificationCenter().setDelegate_(self)
        NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)



def instance():
    return OSXNotification()

