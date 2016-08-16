from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from plyer import brightness


Builder.load_string('''
<BrightnessInterface>:
    orientation: 'vertical'
    BoxLayout:
        BoxLayout:
            orientation: "vertical"
            Slider:
                id: slider
                min: 0
                max: 100
                value: 50
            Label:
                text: str(int(round(slider.value, 0)))
        Button:
            text: "Change!"
            on_release: root.set_bright(value = slider.value, time=200)
    BoxLayout:
        Button:
            text: "Print Brightness"
            on_release: root.get_bright()
        Button:
            text: "Increase Brightness"
            on_release: root.inc_bright(increase_by=10, time=200)
        Button:
            text: "Decrease Brightness"
            on_release: root.dec_bright(decrease_by=10, time=200)

''')


class BrightnessInterface(BoxLayout):

    def set_bright(self, value, time):
        value = round(value, 0)
        brightness.set_brightness(value=value, time=time)

    def get_bright(self):
        print brightness.get_brightness()

    def inc_bright(self, increase_by, time):
        increase_by = round(increase_by, 0)
        brightness.inc_brightness(increase_by=increase_by, time=time)

    def dec_bright(self, decrease_by, time):
        decrease_by = round(decrease_by, 0)
        brightness.dec_brightness(decrease_by=decrease_by, time=time)


class BrightnessApp(App):

    def build(self):
        return BrightnessInterface()

if __name__ == "__main__":
    app = BrightnessApp()
    app.run()
