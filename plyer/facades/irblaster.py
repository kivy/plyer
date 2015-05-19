class IrBlaster(object):
    '''Infrared blaster facade.'''

    @staticmethod
    def periods_to_microseconds(frequency, pattern):
        '''Convert a pattern from period counts to microseconds.
        '''
        period = 1000000. / frequency
        return [period * x for x in pattern]

    @staticmethod
    def microseconds_to_periods(frequency, pattern):
        '''Convert a pattern from microseconds to period counts.
        '''
        period = 1000000. / frequency
        return [x / period for x in pattern]

    @property
    def frequencies(self):
        '''Property which contains a list of frequency ranges
           supported by the device in the form:

           [(from1, to1),
            (from2, to2),
            ...
            (fromN, toN)]
        '''
        return self.get_frequencies()

    def get_frequencies(self):
        return self._get_frequencies()

    def _get_frequencies(self):
        raise NotImplementedError()

    def transmit(self, frequency, pattern, mode='period'):
        '''Transmit an IR sequence.

        :parameters:
            `frequency`: int
                Carrier frequency for the IR transmission.
            `pattern`: list[int]
                Burst pair pattern to transmit.
            `mode`: str, defaults to 'period'
                Specifies the format of the pattern values.
                Can be 'period' or 'microseconds'.
        '''
        return self._transmit(frequency, pattern, mode)

    def _transmit(self, frequency, pattern, mode):
        raise NotImplementedError()

    def exists(self):
        '''Check if the device has an infrared emitter.
        '''
        return self._exists()

    def _exists(self):
        raise NotImplementedError()
