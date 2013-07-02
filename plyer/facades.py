'''
Facades
=======

Interface of all the features availables.

'''

class Accelerometer(object):

    @property
    def acceleration(self):
        return self.get_acceleration()

    def enable(self):
        raise NotImplemented()

    def disable(self):
        raise NotImplemented()

    def get_acceleration(self):
        raise NotImplemented()


class Camera(object):

    def take_picture(self, filename, on_complete):
        '''Ask the OS to capture a picture, and store it at filename.

        When the capture is done, on_complete will be called with the filename
        as argument. If the callback returns True, the filename will be unlink.
        '''
        raise NotImplemented()


class Notification(object):

    def notify(self, title='', message=''):
        raise NotImplemented()

