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
