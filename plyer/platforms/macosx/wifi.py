from plyer.facades import Wifi
from pyobjus.dylib_manager import load_framework, INCLUDE
from pyobjus import autoclass
load_framework(INCLUDE.Foundation)
load_framework(INCLUDE.CoreWLAN)

CWInterface = autoclass('CWInterface')
CWConfiguration = autoclass('CWConfiguration')
CWNetwork = autoclass('CWNetwork')
NSMutableArray = autoclass('NSMutableArray')
CWChannel = autoclass('CWChannel')
CWWiFiClient = autoclass('CWWiFiClient')
NSSortDescriptor = autoclass('NSSortDescriptor')
NSArray = autoclass('NSArray')
NSDictionary = autoclass('NSDictionary')
NSNumber = autoclass('NSNumber')
NSString = autoclass('NSString')


class OSXWifi(Wifi):

    names = {}

    def _is_enabled(self):
        '''
        Returns `True`if the Wifi is enables else `False`.
        '''
        return CWWiFiClient.sharedWiFiClient().interface().powerOn()

    def _enable(self):
        '''
        Method to turn on the Wi-Fi.
        '''
        CWInterface.interface().setPower_error_(True, None)

    def _disabe(self):
        '''
        Method to turn off the Wi-Fi.
        '''
        CWInterface.interface().setPower_error_(False, None)

    def _get_network_info(self, name):
        '''
        Returns all the network information.
        '''
        def ns(x):
            NSString.alloc().initWithUTF8String_(x)

        accessNetworkType = self.names[name].accessNetworkType
        aggregateRSSI = self.names[name].aggregateRSSI
        beaconInterval = self.names[name].beaconInterval
        bssid = self.names[name].bssid.UTF8String()
        countryCode = self.names[name].countryCode
        hasInternet = self.names[name].hasInternet
        hasInterworkingIE = self.names[name].hasInterworkingIE
        hessid = self.names[name].hessid
        ibss = self.names[name].ibss
        isAdditionalStepRequiredForAccess = \
            self.names[name].isAdditionalStepRequiredForAccess
        isCarPlayNetwork = self.names[name].isCarPlayNetwork
        isEmergencyServicesReachable = \
            self.names[name].isEmergencyServicesReachable
        isPasspoint = self.names[name].isPasspoint
        isPersonalHotspot = self.names[name].isPersonalHotspot
        isUnauthenticatedEmergencyServiceAccessible = \
            self.names[name].isUnauthenticatedEmergencyServiceAccessible
        noiseMeasurement = self.names[name].noiseMeasurement
        physicalLayerMode = self.names[name].physicalLayerMode
        rssiValue = self.names[name].rssiValue
        securityType = self.names[name].securityType
        ssid = self.names[name].ssid.UTF8String()
        supportsEasyConnect = self.names[name].supportsEasyConnect
        supportsWPS = self.names[name].supportsWPS
        venueGroup = self.names[name].venueGroup
        venueType = self.names[name].venueType

        return {'accessNetworkType': accessNetworkType,
                'aggregateRSSI': aggregateRSSI,
                'beaconInterval': beaconInterval,
                'bssid': bssid,
                'countryCode': countryCode,
                'hasInternet': hasInternet,
                'hasInternet': hasInternet,
                'hasInterworkingIE': hasInterworkingIE,
                'hessid': hessid,
                'ibss': ibss,
                'isAdditionalStepRequiredForAccess':
                    isAdditionalStepRequiredForAccess,
                'isCarPlayNetwork': isCarPlayNetwork,
                'isEmergencyServicesReachable': isEmergencyServicesReachable,
                'isPasspoint': isPasspoint,
                'isPersonalHotspot': isPersonalHotspot,
                'isUnauthenticatedEmergencyServiceAccessible':
                    isUnauthenticatedEmergencyServiceAccessible,
                'noiseMeasurement': noiseMeasurement,
                'physicalLayerMode': physicalLayerMode,
                'rssiValue': rssiValue,
                'securityType': securityType,
                'ssid': ssid,
                'supportsEasyConnect': supportsEasyConnect,
                'supportsWPS': supportsWPS,
                'venueGroup': venueGroup,
                'venueType': venueType}

    def _start_scanning(self):
        '''
        Starts scanning for available Wi-Fi networks.
        '''
        self.names = {}
        c = CWInterface.interface()
        scan = c.scanForNetworksWithName_error_(None, None)
        cnt = scan.allObjects().count()
        for i in range(cnt):
            self.names[scan.allObjects().objectAtIndex_(i).ssid.UTF8String()] \
                       = scan.allObjects().objectAtIndex_(i)

    def _stop_scanning(self):
        '''
        Can't stop scanning, API not provided by Apple.
        '''
        return

    def _get_available_wifi(self):
        '''
        Returns the name of available networks.
        '''
        return self.names.keys()


def instance():
    return OSXWifi()
