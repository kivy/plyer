'''
Linux USSD implementation
-------------------------
'''

from plyer.facades import USSD
import dbus

DBUS_INTERFACE_PROPERTIES='org.freedesktop.DBus.Properties'
MM_DBUS_SERVICE='org.freedesktop.ModemManager1'
MM_DBUS_PATH='/org/freedesktop/ModemManager1'
MM_DBUS_INTERFACE_MODEM='org.freedesktop.ModemManager1.Modem'
MM_DBUS_INTERFACE_USSD='org.freedesktop.ModemManager1.Modem.Modem3gpp.Ussd'
MM_USSD_STATE = {0: "unknown",
                 1: "idle",
                 2: "active",
                 3: "response"}
bus = dbus.SystemBus()

class USSD(USSD):
    def __init__(self, *args, **kwargs):
        super(USSD, self).__init__(*args, **kwargs)
        self._manager_proxy = bus.get_object(MM_DBUS_SERVICE, MM_DBUS_PATH)
        self._manager_iface = dbus.Interface(self._manager_proxy, dbus_interface="org.freedesktop.DBus.ObjectManager")

    def _get_first_modem_proxy(self):
        modems = self._manager_iface.GetManagedObjects()
        modempath = modems.keys()[0]
        modemproxy = bus.get_object(MM_DBUS_SERVICE, modempath)
        self._check_enabled(modemproxy)

        return modemproxy

    def _check_enabled(self, proxy):
        modem = dbus.Interface(proxy, dbus_interface=MM_DBUS_INTERFACE_MODEM)
        modem_props = dbus.Interface(proxy, dbus_interface=DBUS_INTERFACE_PROPERTIES)

        if modem_props.Get(MM_DBUS_INTERFACE_MODEM, "State") < 5:
            modem.Enable(True)

    def _initiate(self, command):
        proxy = self._get_first_modem_proxy()
        ussd_iface = dbus.Interface(proxy, dbus_interface=MM_DBUS_INTERFACE_USSD)
        # Workaround for Nokia C1-00
        try:
            ussd_iface.Cancel()
            ussd_iface.Respond("")
        except:
            pass
        return str(ussd_iface.Initiate(command))

    def _respond(self, response):
        proxy = self._get_first_modem_proxy()
        ussd_iface = dbus.Interface(proxy, dbus_interface=MM_DBUS_INTERFACE_USSD)
        return str(ussd_iface.Respond(response))

    def _cancel(self):
        proxy = self._get_first_modem_proxy()
        ussd_iface = dbus.Interface(proxy, dbus_interface=MM_DBUS_INTERFACE_USSD)
        return ussd_iface.Cancel()

    def _get_state(self):
        proxy = self._get_first_modem_proxy()
        props = dbus.Interface(proxy, dbus_interface=DBUS_INTERFACE_PROPERTIES)
        state = props.Get(MM_DBUS_INTERFACE_USSD, "State")

        return MM_USSD_STATE[state]

    def _get_network_notification(self):
        proxy = self._get_first_modem_proxy()
        props = dbus.Interface(proxy, dbus_interface=DBUS_INTERFACE_PROPERTIES)
        return str(props.Get(MM_DBUS_INTERFACE_USSD, "NetworkNotification"))

    def _get_network_request(self):
        proxy = self._get_first_modem_proxy()
        props = dbus.Interface(proxy, dbus_interface=DBUS_INTERFACE_PROPERTIES)
        return str(props.Get(MM_DBUS_INTERFACE_USSD, "NetworkRequest"))

def instance():
    return USSD()