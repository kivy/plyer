from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


Builder.load_string('''
#:import screenshot plyer.screenshot
<ScreenShotDemo>:
    screenshot: screenshot
    orientation: 'vertical'
    padding: '50dp'
    spacing: '20dp'
    Label:
        id: location_label
        size_hint_y: None
        height: sp(40)
        text: 'Screenshot Location: ' + str(root.screenshot.file_path)

    Button:
        id: record_button
        text: 'Take Shot'
        on_release: root.take_shot()
''')


class ScreenshotDemo(BoxLayout):
    '''Root Widget.'''
    screenshot = ObjectProperty()

    def take_shot(self):
        self.screenshot.take_shot()


class ScreenshotApp(App):

    def build(self):
        return ScreenshotDemo()

    def on_pause(self):
        return True

if __name__ == "__main__":
    ScreenshotApp().run()
