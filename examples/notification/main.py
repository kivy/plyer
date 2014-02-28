import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from plyer import notification


class NotificationDemo(BoxLayout):

    def do_notify(self, mode='normal'):
        import os
        kwargs = {'title': self.ids.notification_title.text,
                  'message': self.ids.notification_text.text}
        if mode == 'fancy':
            kwargs['app_name'] = "Plyer Notification Example"
            kwargs['app_icon'] = os.path.dirname(os.path.realpath(__file__))\
                + '/plyer-icon.png'
        notification.notify(**kwargs)


class NotificationDemoApp(App):
    def build(self):
        return NotificationDemo()


if __name__ == '__main__':
    NotificationDemoApp().run()

