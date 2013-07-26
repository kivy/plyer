'''
Facades
=======

Interface of all the features availables.

'''

__all__ = ('Accelerometer', 'Camera', 'Notification', 'TTS')


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
        ''' Use text to speech capabilities to speak the message.

        : param message: What to speak
        :type message: str
        '''
        self._speak(message=message)

    # private

    def _speak(self, **kwargs):
        raise NotImplementedError()

