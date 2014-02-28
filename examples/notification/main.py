import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from plyer import notification


class NotificationDemo(BoxLayout):

    def do_notify(self, title, message, **kwargs):
        notification.notify(title, message, kwargs)


class NotificationDemoApp(App):
    def build(self):
        return NotificationDemo()


if __name__ == '__main__':
    NotificationDemoApp().run()

