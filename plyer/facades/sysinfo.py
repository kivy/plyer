class Sysinfo(object):
    ''' Sysinfo facade.
    '''

    def system_info(self):
        return self._system_info()

    def platform_info(self):
        return self._platform_info()

    def processor_info(self):
        return self._processor_info()

    def version_info(self):
        return self._dist_info()

    # private

    def _system_info(self):
        raise NotImplementedError()

    def _platform_info(self):
        raise NotImplementedError()

    def _processor_info(self):
        raise NotImplementedError()

    def _version_info(self):
        raise NotImplementedError()
