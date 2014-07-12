from jnius import autoclass, cast
from plyer.facades import Vibrator
from plyer.platforms.android import activity

Intent = autoclass('android.content.Intent')
Context = autoclass('android.content.Context')
vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)


class AndroidVibrator(Vibrator):
    def _vibrate(self, **kwargs):
        time = kwargs.get('time')

        if vibrator:
            vibrator.vibrate(int(1000 * time))

    def _pattern(self, **kwargs):
        pattern = kwargs.get('pattern')
        repeat = kwargs.get('repeat')

        pattern = [int(1000 * time) for time in pattern]

        if vibrator:
            vibrator.vibrate(pattern, repeat)

    def _exists(self, **kwargs):
        return vibrator.hasVibrator()

    def _cancel(self, **kwargs):
        vibrator.cancel()


def instance():
    return AndroidVibrator()
