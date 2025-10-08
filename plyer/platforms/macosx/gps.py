import threading
import time

from pyobjus import autoclass, protocol
from pyobjus.dylib_manager import INCLUDE, load_framework

from plyer.facades import GPS

load_framework(INCLUDE.CoreLocation)
load_framework(INCLUDE.Foundation)


CLLocationManager = autoclass('CLLocationManager')
NSRunLoop = autoclass('NSRunLoop')
NSObject = autoclass('NSObject')
NSDate = autoclass('NSDate')


class OSXGPS(GPS):
    def __del__(self):
        self._run_loop_thread_allow = False

    def _configure(self):
        if not hasattr(self, '_run_loop_thread'):
            self._run_loop_thread_allow = True
            self._is_running = False

            self._run_loop_thread = threading.Thread(target=self._run_loop)
            self._run_loop_thread.daemon = True
            self._run_loop_thread.start()

    def _run_loop(self):
        self._location_manager = CLLocationManager.alloc().init()
        self._location_manager.setDelegate_(self)
        self._location_manager.desiredAccuracy = -1.0

        self._location_manager.requestAlwaysAuthorization()
        self._run_loop = NSRunLoop.currentRunLoop()

        while self._run_loop_thread_allow:
            if self._is_running:
                next_date = NSDate.dateWithTimeIntervalSinceNow_(0.01)
                self._run_loop.runMode_beforeDate_('NSDefaultRunLoopMode', next_date)
            time.sleep(0.1)

    def _start(self, **kwargs):
        if not hasattr(self, '_location_manager'):
            self.on_status('provider-disabled', 'standard-macos-provider: denied')
            return

        min_distance = kwargs.get('minDistance')
        self._location_manager.distanceFilter = min_distance

        if self._location_manager.authorizationStatus == 2:
            if self.on_status:
                self.on_status('provider-disabled', 'standard-macos-provider: denied')

        self._location_manager.startUpdatingLocation()
        self._is_running = True

    def _stop(self):
        if hasattr(self, '_location_manager'):
            self._location_manager.stopUpdatingLocation()
        self._is_running = False

    @protocol('CLLocationManagerDelegate')
    def locationManager_didChangeAuthorizationStatus_(self, manager, status):
        if self.on_status:
            s_status = ''
            provider_status = ''
            provider = 'standard-macos-provider'
            if status == 0:
                provider_status = 'provider-disabled'
                s_status = 'notDetermined'
            elif status == 1:
                provider_status = 'provider-enabled'
                s_status = 'restricted'
            elif status == 2:
                provider_status = 'provider-disabled'
                s_status = 'denied'
            elif status == 3:
                provider_status = 'provider-enabled'
                s_status = 'authorizedAlways'
            elif status == 4:
                provider_status = 'provider-enabled'
                s_status = 'authorizedWhenInUse'

            self.on_status(provider_status, f'{provider}: {s_status}')

    @protocol('CLLocationManagerDelegate')
    def locationManager_didUpdateLocations_(self, manager, locations):
        location = manager.location

        try:
            description = location.description().UTF8String()
        except Exception:
            description = location.description.UTF8String()

        split_description = description.split('<')[-1].split('>')[0].split(',')

        lat, lon = [float(coord) for coord in split_description]
        acc = float(description.split(' +/- ')[-1].split('m ')[0])

        self.on_location(
            **{
                'lat': lat,
                'lon': lon,
                'altitude': location.altitude,
                'speed': location.speed,
                'course': location.course,
                'acc': acc,
            },
        )


def instance():
    return OSXGPS()
