from os.path import dirname
from os.path import join
from os.path import realpath

import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from plyer import notification
from plyer.utils import platform


class NotificationDemo(BoxLayout):

    def do_notify(self, mode='normal'):
        kwargs = {'title': self.ids.notification_title.text,
                  'message': self.ids.notification_text.text}
        if mode == 'fancy':
            kwargs['app_name'] = "Plyer Notification Example"
            if platform == "win":
                kwargs['app_icon'] = join(dirname(realpath(__file__)),
                                          'plyer-icon.ico')
                kwargs['timeout'] = 4
            else:
                kwargs['app_icon'] = join(dirname(realpath(__file__)),
                                          'plyer-icon.png')
        notification.notify(**kwargs)


class NotificationDemoApp(App):
    def build(self):
        return NotificationDemo()


if __name__ == '__main__':
    NotificationDemoApp().run()

