'''
Notification
===========

The :class:`Notification` provides access to public methods to create
notifications.

Simple Examples
---------------

To send notification::

    >>> from plyer import notification
    >>> title = 'plyer'
    >>> message = 'This is an example.'
    >>> notification.notify(title=title, message=message)

Supported Platforms
-------------------
Android, Windows, OS X, Linux

'''


class Notification(object):
    # pylint: disable=too-few-public-methods
    '''
    Notification facade.
    '''

    def notify(self, title='', message='', app_name='', app_icon='',
               timeout=10, ticker=''):
        # pylint: disable=too-many-arguments
        '''
        Send a notification.

        :param title: Title of the notification
        :param message: Message of the notification
        :param app_name: Name of the app launching this notification
        :param app_icon: Icon to be displayed along with the message
        :param timeout: time to display the message for, defaults to 10
        :param ticker: text to display on status bar as the notification
                       arrives
        :type title: str
        :type message: str
        :type app_name: str
        :type app_icon: str
        :type timeout: int
        :type ticker: str

        .. note::
           When called on Windows, ``app_icon`` has to be a path to
           a file in .ICO format.
        '''

        self._notify(title=title, message=message, app_icon=app_icon,
                     app_name=app_name, timeout=timeout, ticker=ticker)

    # private

    def _notify(self, **kwargs):
        raise NotImplementedError("No usable implementation found!")
