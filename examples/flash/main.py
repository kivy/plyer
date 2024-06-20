from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from plyer import flash

Builder.load_string('''
<FlashInterface>:
    Button:
        text: "Turn On"
        on_release: root.turn_on()

    Button:
        text: "Turn off"
        on_release: root.turn_off()

    Button:
        text: "Release"
        on_release: root.release()

<ErrorPopup>:
    title: "Error!"
    size_hint: .5, .5
    Label:
        text: "Feature not available for this platform !"

''')


class ErrorPopup(Popup):
    pass


class FlashInterface(BoxLayout):

    def turn_on(self):
        try:
            flash.on()
        except NotImplementedError:
            popup = ErrorPopup()
            popup.open()

    def turn_off(self):
        try:
            flash.off()
        except NotImplementedError:
            popup = ErrorPopup()
            popup.open()

    def release(self):
        try:
            flash.release()
        except NotImplementedError:
            popup = ErrorPopup()
            popup.open()


class FlashApp(App):

    def build(self):
        return FlashInterface()

    def on_pause(self):
        return True


if __name__ == "__main__":
    app = FlashApp()
    app.run()
