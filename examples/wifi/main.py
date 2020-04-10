from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from plyer import wifi
from functools import partial


Builder.load_string('''
<WifiInterface>:
    orientation: 'vertical'
    padding: '30dp'
    spacing: '20dp'
    GridLayout:
        cols: 2
        padding: 20
        spacing: 20
        size_hint: 1,.4
        Button:
            text: "Disconnect"
            on_release: root.disconnect()
        TextInput:
            id: password
            hint_text: "Password"
            disabled: True

    Label:
        size_hint_y: None
        height: sp(20)
        text: 'Wifi enabled: ' + str(root.is_enabled())

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.3
        Button:
            id: wifi_button
            size_hint_y: None
            height: sp(35)
            text: 'Enable Wifi / Start Scanning'
            on_release: root.start_wifi()

        Button:
            id: stop_wifi_button
            size_hint_y: None
            height: sp(35)
            disabled: True
            text: 'Disable Wifi'
            on_release: root.stop_wifi()

    BoxLayout:
        id: scan_layout
        orientation: 'vertical'
        Label:
            size_hint_x: 1
            size_hint_y: None
            valign: 'middle'
            height: '35dp'
            text: 'Scan Results'
''')


class WifiInterface(BoxLayout):

    param = {}

    def _create_popup(self, title, content):
        return Popup(
            title=title,
            content=Label(text=content),
            size_hint=(.8, 1),
            auto_dismiss=True
        )

    def start_wifi(self):
        wifi_button = self.ids['wifi_button']
        wifi_button.text = 'Showing Scan Results'
        wifi_button.on_release = self.show_wifi_scans
        wifi.start_scanning()
        stop_wifi_button = self.ids['stop_wifi_button']
        stop_wifi_button.disabled = False
        text_inpt = self.ids['password']
        text_inpt.disabled = False

    def stop_wifi(self):
        stop_wifi_button = self.ids['stop_wifi_button']
        stop_wifi_button.disabled = True

        wifi_button = self.ids['wifi_button']
        wifi_button.text = 'Enable Wifi'
        wifi_button.on_release = self.start_wifi

        wifi.disable()
        self.ids['scan_layout'].clear_widgets()
        text_inpt = self.ids['password']
        text_inpt.disabled = False

    def start_scanning(self):
        wifi.start_scanning()

    def show_wifi_scans(self):
        stack = self.ids['scan_layout']
        stack.clear_widgets()
        wifi_scans = wifi.names.keys()
        for name in wifi_scans:
            content = ""
            items = wifi._get_network_info(name)
            for key, value in items.items():
                content += "{}:    {} \n".format(key, value)

            popup = self._create_popup(name, content)
            boxl = BoxLayout(orientation='horizontal')
            button = Button(
                text=name,
                size_hint=(1, 1),
                height='40dp',
                on_release=popup.open,
            )
            button_connect = Button(
                text="Connect",
                size_hint_x=.2,
                on_release=partial(self.connect, name))

            boxl.add_widget(button)
            boxl.add_widget(button_connect)
            stack.add_widget(boxl)

    def is_enabled(self):
        return wifi.is_enabled()

    def disconnect(self):
        wifi.disconnect()

    def connect(self, network_name, instance):
        self.param['password'] = self.ids['password'].text
        wifi.connect(network_name, self.param)


class WifiApp(App):

    def build(self):
        return WifiInterface()

    def on_pause(self):
        return True


if __name__ == "__main__":
    WifiApp().run()
