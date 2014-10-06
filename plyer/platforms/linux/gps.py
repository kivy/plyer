'''
Linux GPS
---------
'''

from __future__ import absolute_import

from plyer.facades import GPS
import gps
import os
import sys
import threading
import time

class GPSPoller(threading.Thread):
    def __init__(self, gpsd, callback=None):
        threading.Thread.__init__(self)
        if callback == None:
            del callback
            def callback(*args, **kwargs):
                pass
        self._callback = callback
        self._gpsd = gpsd
        self._running = True
 
    def run(self):
        self._gpsd.send('?WATCH={"enable":true,"json":true};')
        while self._running:
            self._gpsd.next()
            # I don't know how to calculate the bearing
            kw = {"lat":      self._gpsd.fix.latitude,
                  "lon":      self._gpsd.fix.longitude,
                  "speed":    self._gpsd.fix.speed,
                  "altitude": self._gpsd.fix.altitude}
            self._callback(**kw)
            time.sleep(0.1)

    def stop(self):
        self._running = False
        self._gpsd.send('?WATCH={"enable":false};')
 

class LinuxGPS(GPS):
    def _configure(self):
        pass

    def _start(self):
        self._gpsd = gps.gps(mode=gps.WATCH_ENABLE)
        self._poller = GPSPoller(gpsd=self._gpsd, callback=self.on_location)
        self._poller.start()

    def _stop(self):
        self._poller.stop()
        self._poller.join()
        del self._poller


def instance():
    return LinuxGPS()
