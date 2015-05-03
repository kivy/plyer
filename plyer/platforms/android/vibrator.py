'''Implementation Vibrator for Android.'''

from jnius import autoclass
from plyer.facades import Vibrator
from plyer.platforms.android import activity
from plyer.platforms.android import SDK_INT

Context = autoclass('android.content.Context')
vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)


class AndroidVibrator(Vibrator):
    '''Android Vibrator class.

    Supported features:
        * vibrate for some period of time.
        * vibrate from given pattern.
        * cancel vibration.
        * check whether Vibrator exists.
    '''

    def _vibrate(self, time=1):
        if vibrator:
            vibrator.vibrate(int(1000 * time))

    def _pattern(self, pattern=(0, 1), repeat=-1):
        pattern = [int(1000 * time) for time in pattern]

        if vibrator:
            vibrator.vibrate(pattern, repeat)

    def _exists(self):
        if SDK_INT >= 11:
            return vibrator.hasVibrator()
        elif activity.getSystemService(Context.VIBRATOR_SERVICE) is None:
            raise NotImplementedError()
        return True

    def _cancel(self):
        vibrator.cancel()


def instance():
    '''Returns Vibrator with android features.

    :return: instance of class AndroidVibrator
    '''
    return AndroidVibrator()
