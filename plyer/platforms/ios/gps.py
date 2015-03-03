'''
iOS GPS
-----------
'''
import logging
from pyobjus import autoclass, protocol
from pyobjus.dylib_manager import load_framework
from plyer.facades import GPS

load_framework('/System/Library/Frameworks/CoreLocation.framework')
CLLocationManager = autoclass('CLLocationManager')


class iOSGPS(GPS):
    def _configure(self):
        if not hasattr(self, '_location_manager'):
            self._location_manager = CLLocationManager.alloc().init()

    def _start(self):
        self._location_manager.delegate = self
        
        self._location_manager.requestWhenInUseAuthorization() # NSLocationWhenInUseUsageDescription, goes to pause mode
        self._location_manager.startUpdatingLocation()

    def _stop(self):
        self._location_manager.stopUpdatingLocation()
        
    @protocol('CLLocationManagerDelegate')
    def locationManager_didUpdateLocations_(self, manager, locations):
        logging.info("locatino updated")
        
        location = locations.lastObject #.objectAtIndex(locations.count() - 1) # last one is the most recent
        location = manager.location
        logging.info(str(dir(location)))
        logging.info(str(dir(location.coordinate)))
        
        self.on_location(
            lat=location.coordinate.a,
            lon=location.coordinate.b,
            speed=location.speed,
            bearing=location.course, # TODO:
            altitude=location.altitude)


def instance():
    return iOSGPS()
