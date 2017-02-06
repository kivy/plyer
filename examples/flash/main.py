from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
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

''')


class FlashInterface(BoxLayout):

    def turn_on(self):
        try:
            flash.on()
        except NotImplementedError:
            self.ErMsg = "Feature under development for this platform!"
            popup = Popup(title="Error!",
                          content=Label(text=self.ErMsg),
                          size_hint=(None, None), size=(350, 350))
            popup.open()

    def turn_off(self):
        try:
            flash.off()
        except NotImplementedError:
            self.ErMsg = "Feature under development for this platform!"
            popup = Popup(title="Error!",
                          content=Label(text=self.ErMsg),
                          size_hint=(None, None), size=(350, 350))
            popup.open()

    def release(self):
        try:
            flash.release()
        except NotImplementedError:
            self.ErMsg = "Feature under development for this platform!"
            popup = Popup(title="Error!",
                          content=Label(text=self.ErMsg),
                          size_hint=(None, None), size=(350, 350))
            popup.open()


class FlashApp(App):

    def build(self):
        return FlashInterface()

if __name__ == "__main__":
    app = FlashApp()
    app.run()
