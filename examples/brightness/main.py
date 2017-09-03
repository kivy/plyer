from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.lang import Builder
from plyer import brightness
from kivy.uix.button import Button
from kivy.properties import NumericProperty

Builder.load_string('''
<BrightnessInterface>:
    orientation: 'vertical'
    Label:
        text: 'Adjust the slider to increase \\n or decrease the brightness'
    Slider:
        id: slider
        min: 0
        max: 100
        value: root.get_current_brightness()
        on_value: root.set_brightness(slider.value)
    Label:
        text: 'Current brightness = ' + str(slider.value)
''')


class BrightnessInterface(BoxLayout):

    def set_brightness(self, level):
        brightness.set_level(level)

    def get_current_brightness(self):
        return brightness.current_level()


class BrightnessApp(App):

    def build(self):
        return BrightnessInterface()


if __name__ == '__main__':
    BrightnessApp().run()
