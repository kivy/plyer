#!/usr/bin/python
# -*- coding: utf-8 -*-


class MFU(object):
    '''
    A constant describing an uncalibrated magnetic field sensor type.

    Similar to MagneticField but the hard iron calibration (device calibration
    due to distortions that arise from magnetized iron, steel or permanent
    magnets on the device) is not considered in the given sensor values.
    However, such hard iron bias values are returned to you separately in the
    result values so you may use them for custom calibrations.

    Also, no periodic calibration is performed (i.e. there are no
    discontinuities in the data stream while using this sensor) and assumptions
    that the magnetic field is due to the Earth's poles is avoided, but factory
    calibration and temperature compensation have been performed.

    Constant Value: 14 (0x0000000e)
    '''

    @property
    def field(self):
        '''
        Property that returns the current value of Uncalibrated Magnetic Field

        In addition to the magnetic field, the uncalibrated magnetometer also
        provides the estimated hard iron bias in each axis.

        Along x-axis: Geomagnetic field strength (without hard iron
                      calibration) along the x axis in μT.
        Along y-axis: Geomagnetic field strength (without hard iron
                      calibration) along the y axis in μT.
        Along z-axis: Geomagnetic field strength (without hard iron
                      calibration) along the z axis in μT.

        Along x-axis: Iron bias estimation along the x axis in μT.
        Along y-axis: Iron bias estimation along the y axis in μT.
        Along z-axis: Iron bias estimation along the z axis in μT.

        Returns (None, None, None, None, None, None) if no data is currently
        available.
        '''
        return self._get_field() or (None, None, None, None, None, None)

    def enable_listener(self):
        '''
        Enable the Magnetic Field Uncalibrated sensor.
        '''
        self._enable_listener()

    def disable_listener(self):
        '''
        Disable the Magnetic Field Uncalibrated sensor.
        '''
        self._disable_listener()

    #private

    def _get_field(self):
        raise  NotImplementedError()

    def _enable_listener(self, **kwargs):
        raise NotImplementedError()

    def _disable_listener(self, **kwargs):
        raise NotImplementedError()
