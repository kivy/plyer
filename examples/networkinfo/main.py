'''
Network Informaion Example.
'''

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.popup import Popup
from plyer import networkinfo

Builder.load_string('''
#: import networkinfo plyer.networkinfo
<NetworkInfoInterface>:
    orientation: 'vertical'
    BoxLayout:
        Button:
            text: 'Extra Information'
            on_press: extrainfo.text = networkinfo.get_extra_info()
        Label:
            id: extrainfo
    BoxLayout:
        Button:
            text: 'Subtype of Network'
            on_press: subtype.text = networkinfo.get_subtype_name()
        Label:
            id: subtype
    BoxLayout:
        Button:
            text: 'Type of Network'
            on_press: type.text = networkinfo.get_type_name()
        Label:
            id: type
    BoxLayout:
        Button:
            text: 'Is Available?'
            on_press: available.text = str(networkinfo.is_available())
        Label:
            id: available
    BoxLayout:
        Button:
            text: 'Is Connected?'
            on_press: connect.text = str(networkinfo.is_connected())
        Label:
            id: connect
    BoxLayout:
        Button:
            text: 'Roaming'
            on_press: roaming.text = str(networkinfo.is_roaming())
        Label:
            id: roaming
''')


class NetworkInfoInterface(BoxLayout):
    pass


class NetworkInfoApp(App):

    def build(self):
        return NetworkInfoInterface()

if __name__ == "__main__":
    NetworkInfoApp().run()
