class Sms(object):
    '''Sms facade.

    .. note::

        On Android your app needs the SEND_SMS permission in order to
        send sms messages.

    .. versionadded:: 1.2.0

    '''

    def send(self, recipient, message):
        self._send(recipient=recipient, message=message)

    # private

    def _send(self, **kwargs):
        raise NotImplementedError()
