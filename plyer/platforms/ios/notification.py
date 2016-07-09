'''
iOS Notification
'''

from plyer.facades import Notification
from pyobjus import autoclass

UILocalNotification = autoclass('UILocalNotification')
UIUserNotificationSettings = autoclass('UIUserNotificationSettings')
UIApplication = autoclass('UIApplication')
NSDate = autoclass('NSDate')
NSTimeZone = autoclass('NSTimeZone')
UIDevice = autoclass('UIDevice')
UIAlertView = autoclass('UIAlertView')
NSString = autoclass('NSString')
UIAlertController = autoclass('UIAlertController')
UIAlertAction = autoclass('UIAlertAction')


class IosNotification(Notification):

    def _notify(self, **kwargs):

        def ns(x):
            NSString.alloc().initWithUTF8String_(x)

        local_noti = UILocalNotification.alloc().init()

        local_noti.fireDate = NSDate.date().dateByAddingTimeInterval_(5)
        local_noti.alertBody = ns(kwargs.get('message'))
        local_noti.alertTitle = ns(kwargs.get('title'))
        local_noti.alertAction = ns("Slide to unlock")
        # local_noti.timeZone = "GMT+5"
        local_noti.applicationIconBadgeNumber = 10

        if UIDevice.currentDevice().systemVersion.floatValue < 8.0:
            UIApplication.sharedApplication() \
                .scheduleLocalNotification_(local_noti)
            return

        # settings = UIUserNotificationSettings.settingsForTypes_categories_(0 | 1 << 0 | 1 << 1 | 1 << 2,
        #                                                                    None)
        settings = UIUserNotificationSettings \
            .settingsForUserNotificationTypes_userNotificationActionSettings_(0 | 1 << 0 | 1 << 1 | 1 << 2,
                                                                              None)
        UIApplication.sharedApplication() \
            .registerUserNotificationSettings_(settings)
        UIApplication.sharedApplication() \
            .registerForRemoteNotifications(settings)
        # UIApplication.sharedApplication() \
        #    .presentLocalNotificationNow_(local_noti)
        UIApplication.sharedApplication() \
            .scheduleLocalNotification_(local_noti)


def instance():
    return IosNotification()
