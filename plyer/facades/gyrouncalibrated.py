class GyroUncalibrated(object):
    '''
    A constant describing an uncalibrated gyroscope sensor type.

    Similar to Gyroscope but no gyro-drift compensation has been performed to
    adjust the given sensor values. However, such gyro-drift bias values are
    returned to you separately in the result values so you may use them for
    custom calibrations.

    Factory calibration and temperature compensation is still applied to the
    rate of rotation (angular speeds).

    Constant Value: 16 (0x00000010)
    '''

    @property
    def rotation(self):
        '''
        Property that returns the current rate of rotation around the X, Y and
        Z axis. An estimation of the drift on each axis is reported as well.

        Rotation is positive in the counter-clockwise direction
        (right-hand rule). That is, an observer looking from some positive
        location on the x, y or z axis at a device positioned on the origin
        would report positive rotation if the device appeared to be rotating
        counter clockwise.

        Along x-axis: angular speed (w/o drift compensation) around the X axis
                      in rad/s
        Along y-axis: angular speed (w/o drift compensation) around the Y axis
                      in rad/s
        Along z-axis: angular speed (w/o drift compensation) around the Z axis
                      in rad/s

        Along x-axis: estimated drift around X axis in rad/s
        Along y-axis: estimated drift around Y axis in rad/s
        Along z-axis: estimated drift around Z axis in rad/s

        Returns (None, None, None, None, None, None) if no data is currently
        available.
        '''
        return self._get_rotation() or (None, None, None, None, None, None)

    def enable_listener(self):
        '''
        Enable the Gyroscope Uncalibrated sensor.
        '''
        self._enable_listener()

    def disable_listener(self):
        '''
        Disable the Gyroscope Uncalibrated sensor.
        '''
        self._disable_listener()

    #private

    def _get_rotation(self):
        raise  NotImplementedError()

    def _enable_listener(self, **kwargs):
        raise NotImplementedError()

    def _disable_listener(self, **kwargs):
        raise NotImplementedError()
