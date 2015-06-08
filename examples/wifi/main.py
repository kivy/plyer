from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

from wifi import instance

Builder.load_string('''
<WifiInterface>:
    orientation: 'vertical'
    padding: '30dp'
    spacing: '20dp'

    Label:
        size_hint_y: None
        height: sp(20)
        text: 'Wifi enabled: ' + str(root.wifi.is_enabled())

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.3
        Button:
            id: wifi_button
            size_hint_y: None
            height: sp(35)
            text: 'Enable Wifi'
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
    """Main Layout."""

    wifi = instance()

    def _create_popup(self, title, content):
        return Popup(
            title=title,
            content=Label(text=content),
            size_hint=(1, 1),
            auto_dismiss=True
        )

    def start_wifi(self):
        wifi_button = self.ids['wifi_button']
        wifi_button.text = 'Show Scan Results'
        wifi_button.on_release = self.show_wifi_scans
        self.wifi.enable()

        stop_wifi_button = self.ids['stop_wifi_button']
        stop_wifi_button.disabled = False

    def stop_wifi(self):
        stop_wifi_button = self.ids['stop_wifi_button']
        stop_wifi_button.disabled = True

        wifi_button = self.ids['wifi_button']
        wifi_button.text = 'Enable Wifi'
        wifi_button.on_release = self.start_wifi

        self.wifi.disable()
        self.ids['scan_layout'].clear_widgets()

    def show_wifi_scans(self):
        wifi_scans = self.wifi.get_access_points()
        if not wifi_scans:
            return

        stack = self.ids['scan_layout']
        stack.clear_widgets()
        scan_format = "SSID: %s\nBSSID: %s\nLevel: %s\n"

        for s in wifi_scans:
            popup = self._create_popup(
                s['ssid'],
                scan_format % (s['ssid'], s['bssid'], s['level'])
            )

            button = Button(
                text=s['ssid'],
                size_hint_y=None,
                height='40dp',
                on_release=popup.open,
            )
            stack.add_widget(button)


class WifiApp(App):
    """Main App."""

    def build(self):
        """Return root layout."""
        interface = WifiInterface()
        return interface


if __name__ == "__main__":
    WifiApp().run()
