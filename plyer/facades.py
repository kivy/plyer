'''
Facades
=======

Interface of all the features availables.

'''

__all__ = ('Accelerometer', 'Camera', 'GPS', 'Notification',
           'TTS', 'Email', 'Vibrator', 'Orientation')


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

    def notify(self, title='', message='', app_name='', app_icon='',
                timeout=10):
        '''Send a notification.

        :param title: Title of the notification
        :param message: Message of the notification
        :param app_name: Name of the app launching this notification
        :param app_icon: Icon to be displayed along with the message
        :param timeout: time to display the message for, defaults to 10
        :type title: str
        :type message: str
        :type app_name: str
        :type app_icon: str
        :type timeout: int
        '''
        self._notify(title=title, message=message, app_icon=app_icon,
                     app_name=app_name, timeout=timeout)

    # private

    def _notify(self, **kwargs):
        raise NotImplementedError("No usable implementation found!")


class Email(object):
    '''Email facade.'''

    def send(self, recipient=None, subject=None, text=None,
             create_chooser=None):
        '''Open an email client message send window, prepopulated with the
        given arguments.

        :param recipient: Recipient of the message (str)
        :param subject: Subject of the message (str)
        :param text: Main body of the message (str)
        :param create_chooser: Whether to display a program chooser to
                               handle the message (bool)

        .. note:: create_chooser is only supported on Android
        '''
        self._send(recipient=recipient, subject=subject, text=text,
                   create_chooser=create_chooser)

    # private

    def _send(self, **kwargs):
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


class Vibrator(object):
    '''Vibration facade.

    .. note::
        On Android your app needs the VIBRATE permission to
        access the vibrator.

    '''

    def vibrate(self, time=1):
        '''Ask the vibrator to vibrate for the given period.

        :param time: Time to vibrate for, in seconds. Default is 1.
        '''
        self._vibrate(time=time)

    def _vibrate(self, **kwargs):
        raise NotImplementedError()

    def pattern(self, pattern=[0, 1], repeat=-1):
        '''Ask the vibrator to vibrate with the given pattern, with an
        optional repeat.

        :param pattern: Pattern to vibrate with. Should be a list of
        times in seconds. The first number is how long to wait before
        vibrating, and subsequent numbers are times to vibrate and not
        vibrate alternately. Defaults to ``[0, 1]``.

        :param repeat: Index at which to repeat the pattern. When the
        vibration pattern reaches this index, it will start again from
        the beginning. Defaults to ``-1``, which means no repeat.
        '''
        self._pattern(pattern=pattern, repeat=repeat)

    def _pattern(self, **kwargs):
        raise NotImplementedError()

    def exists(self):
        '''Check if the device has a vibrator. Returns True or False.'''
        return self._exists()

    def _exists(self, **kwargs):
        raise NotImplementedError()

    def cancel(self):
        '''Cancels any current vibration, and stops the vibrator.'''
        self._cancel()

    def _cancel(self, **kwargs):
        raise NotImplementedError()


class Orientation(object):
    '''Orientation facade.

    .. note::
        These settings are generally guidelines, the operating
        system may choose to ignore them, or they may be overridden by
        other system components.
    '''

    def set_landscape(self, reverse=False):
        '''Rotate the app to a landscape orientation.

        :param reverse: If True, uses the opposite of the natural
                        orientation.
        '''
        self._set_landscape(reverse=reverse)

    def _set_landscape(self, **kwargs):
        raise NotImplementedError()

    def set_portrait(self, reverse=False):
        '''Rotate the app to a portrait orientation.

        :param reverse: If True, uses the opposite of the natural
                        orientation.
        '''
        self._set_portrait(reverse=reverse)

    def _set_portrait(self, **kwargs):
        raise NotImplementedError()

    def set_sensor(self, mode='any'):
        '''Rotate freely following sensor information from the device.

        :param mode: The rotation mode, should be one of 'any' (rotate
                     to any orientation), 'landscape' (choose nearest
                     landscape mode) or 'portrait' (choose nearest
                     portrait mode). Defaults to 'any'.
        '''
        self._set_sensor(mode=mode)

    def _set_sensor(self, **kwargs):
        raise NotImplementedError()
