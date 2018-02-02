from os.path import dirname
from os.path import join
from os.path import realpath

import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from plyer import notification
from plyer.utils import platform
from plyer.compat import PY2


class NotificationDemo(BoxLayout):

    def do_notify(self, mode='normal'):
        title = self.ids.notification_title.text
        message = self.ids.notification_text.text
        ticker = self.ids.ticker_text.text
        if PY2:
            title = title.decode('utf8')
            message = message.decode('utf8')
        kwargs = {'title': title, 'message': message, 'ticker': ticker}

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

    def on_pause(self):
        return True


if __name__ == '__main__':
    NotificationDemoApp().run()
