class Sms(object):
    '''Sms facade.

    .. note::

        On Android your app needs the SEND_SMS permission in order to
        send sms messages.
        It does not require any permission to use the edit method.

    .. versionadded:: 1.2.0

    '''

    def send(self, recipient, message):
        self._send(recipient=recipient, message=message)

    def edit(self, recipient=None, message=None):
        self._edit(recipient=recipient, message=message)

    # private

    def _send(self, **kwargs):
        raise NotImplementedError()

    def _edit(self, **kwargs):
        raise NotImplementedError()