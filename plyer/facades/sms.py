class Sms(object):
    '''Sms facade.

    .. note::

        On Android your app needs the following permission to achieve desired
        task.

        - SEND_SMS: permission in order to send sms messages.

        - RECEIVE_SMS: Permission to reveive SMS.

        - READ_SMS: Permission to read SMS from the Inbox.

    '''

    def send(self, recipient, message):
        self._send(recipient=recipient, message=message)

    @property
    def phonenumber(self):
        '''
        Get the number of the sender.
        '''
        return self.get_phonenumber()

    def get_phonenumber(self):
        self._get_phonenumber()

    @property
    def message(self):
        '''
        Get the Number of the sender.
        '''
        return self.get_message()

    def get_message(self):
        self._get_message()

    # private

    def _send(self, **kwargs):
        raise NotImplementedError()

    def _get_phonenumber(self):
        raise NotImplementedError()

    def _get_message(self):
        raise NotImplementedError()
