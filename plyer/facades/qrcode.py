'''
QRCode Facade.
=============

The :class:`QRCode` is to provide suite of tools for handling QR codes in your desktop
devices.
It currently supports scanning code, reading file, encode qr and getting available
qr data type list.

Usage examples
-------------
The following examples explains the use case of QRCode class::
'''


class QRCode(object):
    '''
    QRCode Facade.
    '''
    def get_qr_data_type(self):
        '''
        Return a list of QR data type supported.
        '''
        return self._get_qr_data_type()

    def scan_code(self):
        '''
        Return data after decoding from a Webcam
        '''
        return self._scan_code()

    def scan_file(self, filelocation):
        '''
        Return data after decoding from a File
        '''
        return self._scan_file(filelocation)

    def encode_qr(self, data, data_type, filename=None):
        '''
        Encode data to QR Code
        '''
        return self._encode_qr(data, data_type, filename)

    # private

    def _get_qr_data_type(self):
        raise NotImplementedError()

    def _scan_code(self):
        raise NotImplementedError()

    def _scan_file(self, filelocation):
        raise NotImplementedError()

    def _encode_qr(self, **kwargs):
        raise NotImplementedError()

