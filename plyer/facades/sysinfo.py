from collections import namedtuple

'''
Sysinfo Facade.
 =============

The :class:`Sysinfo` is to provides system information.
It currently provides model_info, system_name, platform_info, processor_info,
version_info, architecture_info, device_name, manufacturer_name,
kernel_version, storage_info and screen_resolution.

Usage example
-------------
The following example explains the use case of Sysinfo class::
#:Python 2.7

from kivy.app import App
from plyer import sysinfo
from kivy.properties import StringProperty


class SysinfoInterface(BoxLayout):

    model_ = StringProperty()

    def __init__(self, **kwargs):
        super(SysinfoInterface, self).__init__(**kwargs)
        self.get_model()

    def get_model(self):
        # calling the method to extract the model information of that device.
        self.model_ = sysinfo.model_info()


class SysinfoApp(App):

    def build(self):
        return SysinfoInterface()

if __name__ == "__main__":
    app = SysinfoApp()
    app.run()


Implementing the UI in kivy language:
-------------------------------------------
#:kivy 1.9.1

<SysinfoInterface>:
    GridLayout:
        cols: 2
        Label:
            text: "Model"
        Label:
            text: root.model_
'''


class Sysinfo(object):
    ''' Sysinfo facade.
    '''
    CpuNamedTuple = namedtuple('cpu_namedtuple',
                               ('model', 'manufacturer', 'cores', 'arch'))

    def model_info(self, alias=True):
        """ returns device model name.
        * **alias** *(boolean)*: on desktop platforms if True allows
        replacing default 'System Product Name' value with
        '<device_name> (<Main Board name>)'. Particularly useful for
        self-assembled machines.
        """
        return self._model_info(alias)

    def system_name(self):
        # returns the name of system.
        return self._system_name()

    def platform_info(self):
        # returns platform name including version.
        return self._platform_info()

    def processor_info(self):
        """returns the processor details as tuple-like object with fields:
        * **model** *(str)*: CPU model name or ''
        * **manufacturer** *(str)*: manufacturer name
        * **arch** *(str)*: architecture info
        * **cores** *(int)*: number of physical cores or None
        """
        return self._processor_info()

    def version_info(self):
        # returns tuple with information of OS name, version and type
        return self._version_info()

    def architecture_info(self):
        # returns architecture of device.
        return self._architecture_info()

    def device_name(self):
        # returns name of the device.
        return self._device_name()

    def manufacturer_name(self, alias=True):
        """ returns device manufacturer name.
        * **alias** *(boolean)*: on desktop platforms if True allows
        replacing default 'System Manufacturer' value with
        main board manufacturer name instead. Particularly useful for
        self-assembled machines.
        """
        return self._manufacturer_name(alias)

    def kernel_version(self):
        # returns the kernel name.
        return self._kernel_version()

    def storage_info(self, path=None):
        """returns the available storage capacity
        on desktop platforms use *path* argument, which defaults
        *'~/' on Linux and Mac
        *'C:' on Windows
        ignored on iOS and Android
        """
        return self._storage_info(path)

    def memory_info(self):
        # return total device system memory (RAM) in bytes (integer)
        return self._memory_info()

    def screen_resolution(self):
        # returns the screen's resolution as 2-tuple, e.g.: (1200,980)
        return self._screen_resolution()

    # private

    def _model_info(self, alias):
        raise NotImplementedError()

    def _system_name(self):
        raise NotImplementedError()

    def _platform_info(self):
        raise NotImplementedError()

    def _processor_info(self):
        raise NotImplementedError()

    def _version_info(self):
        raise NotImplementedError()

    def _architecture_info(self):
        raise NotImplementedError()

    def _device_name(self):
        raise NotImplementedError()

    def _manufacturer_name(self, alias):
        raise NotImplementedError()

    def _kernel_version(self):
        raise NotImplementedError()

    def _storage_info(self, path):
        raise NotImplementedError()

    def _memory_info(self):
        raise NotImplementedError()

    def _screen_resolution(self):
        raise NotImplementedError()
