class Sysinfo(object):
    ''' Sysinfo facade.
    '''

    def model_info(self):
        # returns the model name.
        return self._model_info()

    def system_info(self):
        # returns the name of system.
        return self._system_info()

    def platform_info(self):
        # returns platform name including version.
        return self._platform_info()

    def processor_info(self):
        # returns the processor details
        return self._processor_info()

    def version_info(self):
        # returns release, version and ptype.
        return self._version_info()

    def architecture_info(self):
        # returns architecture of device.
        return self._architecture_info()

    def device_name(self):
        # returns name of the device.
        return self._device_name()

    def manufacturer_name(self):
        # returns the manufacturer's name
        return self._manufacturer_name()

    def kernel_version(self):
        # returns the kernel name.
        return self._kernel_version()

    def storage_info(self):
        # returns the storage capacity o fthe system.
        return self._storage_info()

    def screen_dimension(self):
        # returns the screen dimensiotn like 1200x980.
        return self._screen_dimension()

    # private

    def _model_info(self):
        raise NotImplementedError()

    def _system_info(self):
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

    def _manufacturer_name(self):
        raise NotImplementedError()

    def _kernel_version(self):
        raise NotImplementedError()

    def _storage_info(self):
        raise NotImplementedError()

    def _screen_dimension(self):
        raise NotImplementedError()
