# coding=utf-8


class Flash(object):
    """Flash facade.

    .. versionadded:: 1.2.5

    This can be used to activate the flash of your camera on
    Android and iOS
    """

    def on(self):
        """Activate the flash
        """
        self._on()

    def off(self):
        """Deactiavte the flash
        """
        self._off()

    def release(self):
        """Release any access to the Flash / Camera.
        Call this when you're done using the Flash.
        This will release the Camera, and stop any process.

        Next call to `_on` will reactivate it.
        """
        self._release()

    # private

    def _on(self):
        raise NotImplementedError()

    def _off(self):
        raise NotImplementedError()

    def _release(self):
        pass
