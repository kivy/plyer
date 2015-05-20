"""Utils example.

Shows current sensors, current screen DPI and available connection to internet,
wifi features like scanning for devices.
"""
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from plyer import utils

Builder.load_string('''
<UtilsInterface>:
    orientation: 'vertical'
    padding: '30dp'
    spacing: '20dp'

    Label:
        size_hint_y: None
        height: sp(20)
        text: 'Internet Connection: ' + str(root.hardware.is_connection())
    Label:
        size_hint_y: None
        height: sp(20)
        text: 'Wifi enabled: ' + str(root.hardware.is_wifi_enabled())
    Label:
        size_hint_y: None
        height: sp(20)
        text: 'Display Metrics: ' + str(root.hardware.display_metrics())

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.3
        Button:
            id: wifi_button
            size_hint_y: None
            height: sp(35)
            text: 'Start Wifi'
            on_release: root.start_wifi()

        Button:
            id: stop_wifi_button
            size_hint_y: None
            height: sp(35)
            disabled: True
            text: 'Stop Wifi'
            on_release: root.stop_wifi()

    Button:
        id: button_keyboard
        size_hint_y: None
        height: '35dp'
        text: 'Show Keyboard'
        on_release: root.toggle_keyboard()


    BoxLayout:
        id: sensor_layout
        orientation: 'vertical'
        Label:
            size_hint_x: 1
            size_hint_y: None
            valign: 'middle'
            height: '35dp'
            text: 'Sensors'

''')


class UtilsInterface(BoxLayout):
    """Main Layout."""

    hardware = utils
    keyboard_state = 'hidden'

    def _create_popup(self, title, content):
        return Popup(
            title=title,
            content=Label(text=content),
            size_hint=(1, 1),
            auto_dismiss=True
        )

    def toggle_keyboard(self):
        button_keyboard = self.ids['button_keyboard']
        if self.keyboard_state == 'hidden':
            self.keyboard_state = 'show'
            self.hardware.show_keyboard()
            button_keyboard.text = 'Hide Keyboard'
        else:
            self.keyboard_state = 'hidden'
            self.hardware.hide_keyboard()
            button_keyboard.text = 'Show Keyboard'

    def add_sensors(self):
        sensors = self.hardware.get_hardware_sensors()
        stack = self.ids['sensor_layout']

        for sensor in sensors:
            title = sensor['name']
            content = '\n'.join(
                [key.title() + ' : ' + str(sensor[key]) for key in sensor]
            )
            popup = self._create_popup(title, content)

            button = Button(
                text=title,
                size_hint_y=None,
                height='40dp',
                on_release=popup.open,
            )

            stack.add_widget(button)

    def start_wifi(self):
        wifi_button = self.ids['wifi_button']
        wifi_button.text = 'Show Scan Results'
        wifi_button.on_release = self.show_wifi_scans
        self.hardware.start_wifi()

        stop_wifi_button = self.ids['stop_wifi_button']
        stop_wifi_button.disabled = False

    def stop_wifi(self):
        stop_wifi_button = self.ids['stop_wifi_button']
        stop_wifi_button.disabled = True

        wifi_button = self.ids['wifi_button']
        wifi_button.text = 'Start Wifi'
        wifi_button.on_release = self.start_wifi

        self.hardware.stop_wifi()

    def show_wifi_scans(self):
        wifi_scans = self.hardware.get_wifi_scans()
        if not wifi_scans:
            return
        scan_format = "SSID: %s\nBSSID: %s\nLevel: %s\n"
        popup = self._create_popup(
            'Scan Results',
            '\n'.join([scan_format % (s['ssid'], s['bssid'], s['level'])
                       for s in wifi_scans])
        )
        popup.open()


class UtilsApp(App):
    """Main App."""

    def build(self):
        """Return root layout."""
        interface = UtilsInterface()
        interface.add_sensors()
        return interface


if __name__ == "__main__":
    UtilsApp().run()
