from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout


Builder.load_string('''
#:import screenshot plyer.screenshot
<ScreenshotDemo>:
    orientation: 'vertical'
    padding: '50dp'
    spacing: '20dp'
    Label:
        size_hint_y: None
        height: sp(40)
        text: 'Screenshot Location: ' + str(screenshot.file_path)

    Button:
        text: 'Capture Screenshot'
        on_release: screenshot.capture()
''')


class ScreenshotDemo(BoxLayout):
    '''Root Widget.'''


class ScreenshotApp(App):

    def build(self):
        return ScreenshotDemo()


if __name__ == "__main__":
    ScreenshotApp().run()
