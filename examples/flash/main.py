from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
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
        flash.on()

    def turn_off(self):
        flash.off()

    def release(self):
        flash.release()


class FlashApp(App):

    def build(self):
        return FlashInterface()

    def on_pause(self):
        return True


if __name__ == "__main__":
    app = FlashApp()
    app.run()
