class SmsReceive(object):
    '''Receive Sms facade.
    .. note::
        On Android your app needs the following permission to achieve desired
        task.
        - RECEIVE_SMS: Permission to reveive SMS.
    '''
    def receive(self):
        return self._receive()

    def _receive(self):
        raise NotImplementedError()
