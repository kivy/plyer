#!/usr/bin/python
# -*- coding: utf-8 -*-


class GameRotation(object):
    '''
    Game Rotation vector facade.
    A constant describing an uncalibrated rotation vector sensor type.

    Identical to RotationVector except that it doesn't use the geomagnetic
    field. Therefore the Y axis doesn't point north, but instead to some
    other reference, that reference is allowed to drift by the same order of
    magnitude as the gyroscope drift around the Z axis.

    In the ideal case, a phone rotated and returning to the same real-world
    orientation should report the same game rotation vector (without using
    the earth's geomagnetic field). However, the orientation may drift
    somewhat over time.
    '''

    @property
    def vector(self):
        '''
        Property that returns the current value of Game Rotation Vector.
        Along x-axis: Rotation vector component along the x axis (x * sin(θ/2))
        Along y-axis: Rotation vector component along the y axis (y * sin(θ/2))
        Along z-axis: Rotation vector component along the z axis (z * sin(θ/2))
        Returns (None, None, None) if no data is currently available.
        '''
        return self._get_vector() or (None, None, None)

    def enable_listener(self):
        '''
        Enable the Game Rotation Vector sensor.
        '''
        self._enable_listener()

    def disable_listener(self):
        '''
        Disable the Game Rotation Vector sensor.
        '''
        self._disable_listener()

    #private

    def _get_vector(self):
        raise  NotImplementedError()

    def _enable_listener(self, **kwargs):
        raise NotImplementedError()

    def _disable_listener(self, **kwargs):
        raise NotImplementedError()
