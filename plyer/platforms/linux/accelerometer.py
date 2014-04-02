'''
Linux accelerometer
---------------------
'''

from plyer.facades import Accelerometer
import os
import glob
import re

class LinuxAccelerometer(Accelerometer):

    def _enable(self):
        pass

    def _disable(self):
        pass

    def _get_acceleration(self):
        try:
            pos = glob.glob("/sys/devices/platform/*/position")[0]
        except IndexError:
            # FIXME: decide whether it should return 0,0,0 or raise an exception
            #        when no accelerometer is present.
            return (0, 0, 0)

        with open(pos, "r") as p:
            t = p.read()
            coords = re.findall(r"[-]?\d+\.?\d*", t)
            # Apparently the acceleration on sysfs goes from -1000 to 1000.
            # I divide it by 100 to make it equivalent to Android.
            return [float(i)/100 for i in coords]

def instance():
    return LinuxAccelerometer()
