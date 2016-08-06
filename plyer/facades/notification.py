class Notification(object):
    '''Notification facade.
    '''

    def notify(self, title='', message='', app_name='', app_icon='',
               timeout=10, ticker='', buttons={}):
        '''Send a notification.

        :param title: Title of the notification
        :param message: Message of the notification
        :param app_name: Name of the app launching this notification
        :param app_icon: Icon to be displayed along with the message
        :param timeout: time to display the message for, defaults to 10
        :param ticker: text to display on status bar as the notification
                       arrives
        :param buttons: contains icons and name.
            :param name: str
            :param icon: str
        :type title: str
        :type message: str
        :type app_name: str
        :type app_icon: str
        :type timeout: int
        :type ticker: str
        :type buttons: dict
        '''

        self._notify(title=title, message=message, app_icon=app_icon,
                     app_name=app_name, timeout=timeout, ticker=ticker,
                     buttons=buttons)

    # private

    def _notify(self, **kwargs):
        raise NotImplementedError("No usable implementation found!")
