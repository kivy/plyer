'''
Facades
=======

Interface of all the features availables.

'''

__all__ = ('Accelerometer', 'Camera', 'GPS', 'Notification', 'TTS')


class Accelerometer(object):
    '''Accelerometer facade.
    '''

    @property
    def acceleration(self):
        '''Property that returns values of the current acceleration sensors, as
        a (x, y, z) tuple
        '''
        return self.get_acceleration()

    def enable(self):
        '''Activate the accelerometer sensor
        '''
        self._enable()

    def disable(self):
        '''Disable the accelerometer sensor
        '''
        self._disable()

    def get_acceleration(self):
        return self._get_acceleration()

    # private

    def _enable(self):
        raise NotImplementedError()

    def _disable(self):
        raise NotImplementedError()

    def _get_acceleration(self):
        raise NotImplementedError()


class Camera(object):
    '''Camera facade.
    '''

    def take_picture(self, filename, on_complete):
        '''Ask the OS to capture a picture, and store it at filename.

        When the capture is done, on_complete will be called with the filename
        as argument. If the callback returns True, the filename will be unlink.

        :param filename: Name of the image file
        :param on_complete: Callback that will be called when the operation is
            done

        :type filename: str
        :type on_complete: callable
        '''
        self._take_picture(filename=filename, on_complete=on_complete)

    # private

    def _take_picture(self, **kwargs):
        raise NotImplementedError()


class Notification(object):
    '''Notification facade.
    '''

    def notify(self, title='', message=''):
        '''Send a notification.

        :param title: Title of the notification
        :param message: Message of the notification
        :type title: str
        :type message: str
        '''
        self._notify(title=title, message=message)

    # private

    def _notify(self, **kwargs):
        raise NotImplementedError()


class TTS(object):
    '''TextToSpeech facade.
    '''

    def speak(self, message=''):
        '''Use text to speech capabilities to speak the message.

        :param message: What to speak
        :type message: str
        '''
        self._speak(message=message)

    # private

    def _speak(self, **kwargs):
        raise NotImplementedError()


class GPS(object):
    '''GPS facade.

    .. versionadded:: 1.1

    You need to set a `on_location` callback with the :meth:`configure` method.
    This callback will receive a couple of keywords / value, that might be
    different depending of their availability on the targetted platform.
    Lat and lon are always available.

    - lat: latitude of the last location, in degrees
    - lon: longitude of the last location, in degrees
    - speed: speed of the user, in meters/seconds over ground
    - bearing: bearing in degrees
    - altitude: altitude in meters above the sea level

    Here is an example of the usage of gps::

        from plyer import gps

        def print_locations(**kwargs):
            print 'lat: {lat}, lon: {lon}'.format(**kwargs)

        gps.configure(on_location=print_locations)
        gps.start()
        # later
        gps.stop()
    '''

    def configure(self, on_location, on_status=None):
        '''Configure the GPS object. This method should be called before
        :meth:`start`.

        :param on_location: Function to call when receiving a new location
        :param on_status: Function to call when a status message is received
        :type on_location: callable, multiples keys/value will be passed.
        :type on_status: callable, args are "message-type", "status"

        .. warning::

            The `on_location` and `on_status` callables might be called from
            another thread than the thread used for creating the GPS object.
        '''
        self.on_location = on_location
        self.on_status = on_status
        self._configure()

    def start(self):
        '''Start the GPS locations updates
        '''
        self._start()

    def stop(self):
        '''Stop the GPS locations updates
        '''
        self._stop()

    # private

    def _configure(self):
        raise NotImplementedError()

    def _start(self):
        raise NotImplementedError()

    def _stop(self):
        raise NotImplementedError()


