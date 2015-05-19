from kivy.lang import Builder
from plyer import gps
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import Clock

kv = '''
BoxLayout:
    orientation: 'vertical'

    Label:
        text: app.gps_location

    Label:
        text: app.gps_status

    BoxLayout:
        size_hint_y: None
        height: '48dp'
        padding: '4dp'

        ToggleButton:
            text: 'Start' if self.state == 'normal' else 'Stop'
            on_state:
                app.gps.start() if self.state == 'down' else app.gps.stop()
'''


def mainthread(func):
    # This method is now part of Kivy 1.8.0. When it's released, remove it.
    def delayed_func(*args, **kwargs):
        def callback_func(dt):
            func(*args, **kwargs)
        Clock.schedule_once(callback_func, 0)
    return delayed_func


class GpsTest(App):

    gps_location = StringProperty()
    gps_status = StringProperty('Click Start to get GPS location updates')

    def build(self):
        self.gps = gps
        try:
            self.gps.configure(on_location=self.on_location,
                    on_status=self.on_status)
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            self.gps_status = 'GPS is not implemented for your platform'

        return Builder.load_string(kv)

    @mainthread
    def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

if __name__ == '__main__':
    GpsTest().run()
