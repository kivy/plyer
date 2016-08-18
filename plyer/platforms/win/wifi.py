import plyer.platforms.win.libs.wifi_defs as wifi_lib
from plyer.facades import Wifi


class WindowWifi(Wifi):

    names = {}

    def _is_enabled(self):
        '''
        TODO: Implement this in future
        '''
        return

    def _get_network_info(self, name):
        '''
        Returns all the network information.
        '''
        return wifi_lib.get_network_info(name)

    def _start_scanning(self):
        '''
        Starts scanning for available Wi-Fi networks and returns the available,
        devices.
        '''
        self.names = wifi_lib.start_scanning()

    def _get_available_wifi(self):
        '''
        Returns the name of available networks.
        '''
        return wifi_lib.get_available_wifi()

    def _connect(self, network, parameters):
        '''
        Expects 2 parameters:
            - name/ssid of the network.
            - parameters: dict type
                - bssidList
                - Header
                - uNumOfEntries
                - uTotalNumOfEntries
                - BSSIDs
                - bssType
                - flags
                - password
        '''
        wifi_lib.connect(network, parameters)
        return

    def _disconnect(self):
        '''
        Disconnect from network.
        '''
        wifi_lib.disconnect()
        return


def instance():
    return WindowWifi()
