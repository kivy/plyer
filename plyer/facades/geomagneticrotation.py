#!/usr/bin/python
# -*- coding: utf-8 -*-


class GeomagneticRotation(object):
    '''
    Geomagnetic Rotation Vector facade.
    A constant describing a geo-magnetic rotation vector.

    Similar to RotationVector, but using a magnetometer instead of using a
    gyroscope. This sensor uses lower power than the other rotation vectors,
    because it doesn't use the gyroscope. However, it is more noisy and will
    work best outdoors.

    Constant Value: 20 (0x00000014)
    '''

    @property
    def vector(self):
        '''
        Property that returns the current value of Geomagnetic Rotation Vector.
        Along x-axis: Rotation vector component along the x axis (x * sin(θ/2))
        Along y-axis: Rotation vector component along the y axis (y * sin(θ/2))
        Along z-axis: Rotation vector component along the z axis (z * sin(θ/2))
        Returns (None, None, None) if no data is currently available.
        '''
        return self._get_vector() or (None, None, None)

    def enable_listener(self):
        '''
        Enable the Geomagnetic Rotation Vector sensor.
        '''
        self._enable_listener()

    def disable_listener(self):
        '''
        Disable the Geomagnetic Rotation Vector sensor.
        '''
        self._disable_listener()

    #private

    def _get_vector(self):
        raise  NotImplementedError()

    def _enable_listener(self, **kwargs):
        raise NotImplementedError()

    def _disable_listener(self, **kwargs):
        raise NotImplementedError()
