class QrBarcodeReader(object):
    '''
    QrBarcodeReader facade.
    '''

    def scan(self):
        '''
        Qr and Barcode scanning implementation
        '''
        self._scan()

    # private

    def _scan(self):
        raise NotImplementedError()
