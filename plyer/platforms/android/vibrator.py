'''Implementation Vibrator for Android.'''

from jnius import autoclass
from plyer.facades import Vibrator
from . import activity, SDK_INT

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

    def _vibrate(self, time=None, **kwargs):
        if vibrator:
            vibrator.vibrate(int(1000 * time))

    def _pattern(self, pattern=None, repeat=None, **kwargs):
        pattern = [int(1000 * time) for time in pattern]

        if vibrator:
            vibrator.vibrate(pattern, repeat)

    def _exists(self, **kwargs):
        if SDK_INT >= 11:
            return vibrator.hasVibrator()
        elif activity.getSystemService(Context.VIBRATOR_SERVICE) is None:
            raise NotImplementedError()
        return True

    def _cancel(self, **kwargs):
        vibrator.cancel()


def instance():
    '''Returns Vibrator with android features.

    :return: instance of class AndroidVibrator
    '''
    return AndroidVibrator()
