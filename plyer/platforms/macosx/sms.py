from subprocess import Popen, PIPE
from plyer.facades import Sms as SMS
from plyer.utils import whereis_exe


class OSXSMS(SMS):
    '''
    Implementation of macOS' Messages API
    '''

    def _send(self, **kwargs):
        '''
        Will send `message` to `recipient` via Messages app

        Currently only supports iMessage as macOS can send that standalone
        In order to support SMS, a valid carrier-activated device must be
        connected & configured to macOS
            - activate this by passing in mode='SMS'

        '''

        recipient = kwargs.get('recipient')
        message = kwargs.get('message')
        mode = kwargs.get('mode', 'iMessage')  # can be SMS

        APPLESCRIPT = f"""tell application "Messages"
    set targetService to 1st account whose service type = {mode}
    set targetBuddy to participant "{recipient}" of targetService
    send "{message}" to targetBuddy
end tell"""

        osascript_process = Popen(['osascript', '-e', APPLESCRIPT],
                                stdout=PIPE, stderr=PIPE)
        stdout, stderr = osascript_process.communicate()


def instance():
    import sys
    if whereis_exe('osascript'):
        return OSXSMS()
    sys.stderr.write('osascript not found.')
    return SMS()
