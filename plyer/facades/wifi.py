'''
Wifi Facade.
=============

The :class:`Wifi` is to provide access to the wifi of your mobile/ desktop
devices.
It currently supports enabling, connecting, disconnecting, scanning and
getting network information.

Usage example
-------------
The following example explains the use case of Wifi class::

#:Python 2.7

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from plyer import wifi
from functools import partial


class WifiInterface(BoxLayout):

    def _create_popup(self, title, content):
        # Expects 2 parameters:
        #    - title: title of the popup
        #    - content: content of label in the popup: String type
        # popup contains a Lable diplaying wifi network details.
        return Popup(
            title=title,
            content=Label(text=content),
            size_hint=(.8, 1),
            auto_dismiss=True
        )

    def start_wifi(self):
        # This Method initilaizes the wifi when `start wifi` button is pressed.
        wifi_button = self.ids['wifi_button']
        wifi_button.text = 'Showing Scan Results'
        wifi_button.on_release = self.show_wifi_scans
        if not self.is_enabled():
            wifi.enable()
        wifi.start_scanning()
        stop_wifi_button = self.ids['stop_wifi_button']
        stop_wifi_button.disabled = False
        text_inpt = self.ids['password']
        text_inpt.disabled = False

    def stop_wifi(self):
        # This method stops/disables the wifi when `stop wifi` button is
        # pressed.
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
        # This method is used to start looking for available nearby wifi
        # networks. Extracts all the network information along so following
        # actions could be performed: connecting to that network,
        # disconnecting from that network
        # and getting network information.
        wifi.start_scanning()

    def show_wifi_scans(self):
        # Gets the available wifi network information and displays them in a
        # a BoxLayout with buttons having text as network's ssid.
        stack = self.ids['scan_layout']
        stack.clear_widgets()
        wifi_scans = wifi.names.keys()
        for name in wifi_scans:
            content = ""
            items = wifi._get_network_info(name)
            for key, value in items.iteritems():
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
        # Enables the wifi
        return wifi.is_enabled()

    def disconnect(self):
        # Disables the wifi
        wifi.disconnect()

    def connect(self, network_name, instance):
        # connects with a given network but requires some parameters
        # these parameters are different for each platform
        # Linux:
        #     - expects ssid (name of the network) and a parameter dictionary
        # containing `password` as a key.
        # MacOSX:
        #     - expects ssid (name of the network) and a parameter dictionary
        # containing `password` as a key.
        # Windows:
        #    - Windows part is a little tricky and expects multiple parameters
        # in order to connect to a network, it expects ssid (name of the
        # network) and a parameter dictionary containing following keys.
        #        - bssidList
        #        - Header
        #        - uNumOfEntries
        #        - uTotalNumOfEntries
        #        - BSSIDs
        #        - bssType
        #        - flags
        #        - password
        # These information could be extracted from `get_network_info` method
        wifi.connect(network_name, self.ids['password'].text)


class WifiApp(App):

    def build(self):
        return WifiInterface()


if __name__ == "__main__":
    WifiApp().run()


Implementing the UI in kivy language:
-------------------------------------------
#:kivy 1.9.1

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

'''


class Wifi(object):
    '''Wifi Facade.
    '''

    def is_enabled(self):
        '''
        Returns `True`if the Wifi is enables else `False`.
        '''
        return self._is_enabled()

    def start_scanning(self):
        '''
        Turn on scanning.
        '''
        self._start_scanning()

    def get_network_info(self, name):
        '''
        Return a dictionary of secified network.
        '''
        return self._get_access_points(name=name)

    def get_available_wifi(self):
        '''
        Returns a list of all the available wifi.
        '''
        self._get_available_wifi()

    def connect(self, network, parameters):
        '''
        Method to connect to some network.
        '''
        self._connect(network=network, parameters=parameters)

    def disconnect(self):
        '''
        To disconnect from some network.
        '''
        self._disconnect()

    # private

    def _is_enabled(self):
        raise NotImplementedError()

    def _start_scanning(self):
        raise NotImplementedError()

    def _get_network_info(self, **kwargs):
        raise NotImplementedError()

    def _get_available_wifi(self):
        raise NotImplementedError()

    def _connect(self, **kwargs):
        raise NotImplementedError()

    def _disconnect(self):
        raise NotImplementedError()
