from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from plyer import toast

Builder.load_string('''
<ToastInterface>:
    orientation: 'vertical'
    ToastButton:
        text: 'Short Toast'
        on_release: self.do_toast(self.text, 0)
    ToastButton:
        id: long
        text: "Long Toast"
        on_release: self.do_toast(long.text, 1)
    Label:

''')


class ToastInterface(BoxLayout):
    pass


class ToastButton(Button):

    def do_toast(self, text="", duration=0):
        toast.maketoast(text=text, duration=duration)


class ToastApp(App):

    def build(self):
        return ToastInterface()

if __name__ == "__main__":
    app = ToastApp()
    app.run()
