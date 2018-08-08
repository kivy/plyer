'''
CPU count
=========

Simple Example
---------------

To get CPU count::
    >>> from plyer import cpu
    >>> cpu.cpus  # 1 core, 2 threads, logical = cores * threads
    {'physical': 1, 'logical': 2}

Supported Platforms
-------------------

Linux
'''


class CPU(object):
    '''
    Facade providing info about physical and logical number of processors.
    '''

    @property
    def cpus(self):
        '''
        Property that contains a dict with the following fields:

        * `physical` *(int)*: Total number of physical cores in the system.
        * `logical` *(int)*: Total number of cores * threads in the system.
        '''
        return self._cpus()

    # private

    def _cpus(self):
        raise NotImplementedError()
