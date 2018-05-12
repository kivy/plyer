'''
Volume
=======

Simple Example
---------------
To set the volume::
	>>> import plyer
	>>> plyer.volume.status
	Set Volume(%) : 
	50
	{'Volume_Set': True}

Supported Platforms
-------------------
Linux
'''


class Volume(object):
    '''
    Volume Control info facade.
    '''

    @property
    def status(self):
        return self.get_state()

    def get_state(self):
        return self._get_state()

    # private

    def _get_state(self):
        raise NotImplementedError()
