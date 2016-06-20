class PyNdefRecord(object):
    '''
    Python implemetation of andriod NDefRecords.
    '''

    def create_application_record(self, payload):
        '''
        Create a new application record.
        '''
        self._create_application_record(payload=payload)

    def create_external(self, payload):
        '''
        To encode application specific data into NdefRecord.
        '''
        self._create_external(payload=payload)

    def create_mime(self, payload):
        '''
        To encode MIME type data into NdefRecord like, text/plain,
        image/jpeg, */*. etc
        '''
        self._create_mime(payload=payload)

    def create_text_record(self, payload):
        '''
        To create NdefRecord containing UTF-8 text data.
        '''
        self._create_text_record(payload=payload)

    def create_uri(self, payload):
        '''
        To encode a URI in NdefRecord.
        '''
        self._create_uri(payload=payload)

    def create_RTD_ALTERNATIVE_CARRIER(self, payload):
        '''
        RTD Alternative Carrier type. For use with TNF_WELL_KNOWN.
        '''
        self._create_RTD_ALTERNATIVE_CARRIER(payload=payload)

    def create_RTD_HANDOVER_CARRIER(self, payload):
        '''
        RTD Handover Carrier type. For use with TNF_WELL_KNOWN.
        '''
        self._create_RTD_HANDOVER_CARRIER(payload=payload)

    def create_RTD_HANDOVER_REQUEST(self, payload):
        '''
        RTD Handover Request type. For use with TNF_WELL_KNOWN.
        '''
        self._create_RTD_HANDOVER_REQUEST(payload=payload)

    def create_RTD_HANDOVER_SELECT(self, payload):
        '''
        RTD Handover Select type. For use with TNF_WELL_KNOWN.
        '''
        self._create_RTD_HANDOVER_SELECT(payload=payload)

    def create_RTD_SMART_POSTER(self, payload):
        '''
        RTD Smart Poster type. For use with TNF_WELL_KNOWN.
        '''
        self._create_RTD_SMART_POSTER(payload=payload)

    def create_RTD_TEXT(self, payload):
        '''
        RTD Text type. For use with TNF_WELL_KNOWN.
        '''
        self._create_RTD_TEXT(payload=payload)

    # private

    def _create_application_record(self, **kwargs):
        raise NotImplementedError()

    def _create_external(self, **kwargs):
        raise NotImplementedError()

    def _create_mime(self, **kwargs):
        raise NotImplementedError()

    def _create_text_record(self, **kwargs):
        raise NotImplementedError()

    def _create_uri(self, **kwargs):
        raise NotImplementedError()

    def _create_RTD_ALTERNATIVE_CARRIER(self, **kwargs):
        raise NotImplementedError()

    def _create_RTD_HANDOVER_CARRIER(self, **kwargs):
        raise NotImplementedError()

    def _create_RTD_HANDOVER_REQUEST(self, **kwargs):
        raise NotImplementedError()

    def _create_RTD_HANDOVER_SELECT(self, **kwargs):
        raise NotImplementedError()

    def _create_RTD_SMART_POSTER(self, **kwargs):
        raise NotImplementedError()

    def _create_RTD_TEXT(self, **kwargs):
        raise NotImplementedError()


class NFC(object):
    ''' NFC facade.
    .. note::
        On Android your app needs the NFC permission.

        For Beam, you also need READ_EXTERNAL_SORAGE permission.
    '''
    NdefRecord = PyNdefRecord

    def enable(self):
        '''
        To enable NFC.
        '''
        self._enable()

    def disable(self):
        '''
        to disable NFC.
        '''
        self._disable()

    def write_record(self, ndef_type, payload):
        '''
        Write Android NDefRecord.
        '''
        self._write_record()

    def read_record(self):
        '''
        Read Android NdefRecord.
        '''
        self._read_records()

    def create_ndef_message(self, *records):
        '''
        NdefMessage that will be written on tag.
        '''
        self._create_ndef_message(records=records)

    def read_ndef_message(self, messages):
        '''
        Reading the android NdefMessages.
        '''
        self._read_ndef_messages(messages=messages)

    def set_tag_mode(self, mode):
        '''
        Set the tag mode.
        Choices: `read` or `write`
        '''
        self._set_tag_mode()

    def get_tag_mode(self):
        '''
        Get the tag mode.
        '''
        self._get_tag_mode()

    def read_tag(self):
        '''
        To read the tags detected by NFC.
        '''
        self._read_tag()

    def write_tag(self):
        '''
        To write on tags detected by NFC.
        '''
        self._write_tag()

    def nfc_enable_exchange(self):
        '''
        Enable ndef exchange.
        '''
        self._nfc_enable_exchange()

    def nfc_disable_exchange(self):
        '''
        Disable ndef exchange
        '''
        self._nfc_disable_exchange()

    def nfc_beam(self, files):
        '''
        send files through beam.
        '''
        self._nfc_beam(files=files)

    def on_pause(self):
        '''
        Events called when application is paused.
        '''
        self._on_pause()

    def on_resume(self):
        '''
        Event called when application is resumed.
        '''
        self._on_resume()

    # private

    def _enable(self, **kwargs):
        raise NotImplementedError()

    def _diable(self, **kwargs):
        raise NotImplementedError()

    def _write_record(self, **kwargs):
        raise NotImplementedError()

    def _read_record(self, **kwargs):
        raise NotImplementedError()

    def _create_ndef_message(self, *args):
        raise NotImplementedError()

    def _read_ndef_message(self, **kwargs):
        raise NotImplementedError()

    def _set_tag_mode(self, **kwargs):
        raise NotImplementedError()

    def _get_tag_mode(self, **kwargs):
        raise NotImplementedError()

    def _read_tag(self, **kwargs):
        raise NotImplementedError()

    def _write_tag(self, **kwargs):
        raise NotImplementedError()

    def _nfc_enable_exchange(self, **kwargs):
        raise NotImplementedError()

    def _nfc_disable_exchange(self, **kwargs):
        raise NotImplementedError()

    def _nfc_beam(self, **kwargs):
        raise NotImplementedError()

    def _on_pause(self, **kwargs):
        raise NotImplementedError()

    def _on_resume(self, **kwargs):
        raise NotImplementedError()
