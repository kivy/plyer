from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from plyer.utils import platform


Builder.load_string('''
#:import uniqueid plyer.uniqueid
<UniqueIDInterface>:
    uniqueid: uniqueid
    orientation: 'vertical'
    padding: '50dp'
    spacing: '20dp'
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.3
        Button:
            text: 'Get Unique ID'
            on_release:
                root.get_uid()
    Label:
        text: str(root.text)
    Label:
        text: str(root.uid)
''')


class UniqueIDInterface(BoxLayout):
    '''Root Widget.'''

    uniqueid = ObjectProperty()
    uid = StringProperty()
    text = StringProperty()

    if platform == "android":
        text = "Android ID: "
    elif platform == "ios":
        text = "UUID: "
    elif platform == "win":
        text = "Machine GUID: "
    else:
        text = "Serial Number: "

    def get_uid(self):
        self.uid = self.uniqueid.id or self.uid


class UniqueIDApp(App):

    def build(self):
        return UniqueIDInterface()

    def on_pause(self):
        return True


if __name__ == "__main__":
    UniqueIDApp().run()
