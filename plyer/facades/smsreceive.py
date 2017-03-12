class SmsReceive(object):
    '''Receive Sms facade.
    .. note::
        On Android your app needs the following permission to achieve desired
        task.
        - RECEIVE_SMS: Permission to reveive SMS.
    '''
    def startreceiver(self):
        return self._startreceiver()

#private

    def _startreceiver(self):
        raise NotImplementedError()
