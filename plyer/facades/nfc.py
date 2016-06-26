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

    def create_custom_record(self, payload):
        '''
        To create your own custom records.
        '''
        self._create_custom_record(payload=payload)

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

    def _create_custom_record(self, **kwargs):
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

    def nfc_register(self, tech_list, action_list, data_type):
        '''
        Initializing NFC adapter and listing the techs available.
        '''
        self._nfc_register(tech_list=tech_list, action_list=action_list,
                           data_type=data_type)

    def enable_reader_mode(self):
        '''
        Enables the reader mode for Android Beam.
        '''
        self._enable_reader_mode()

    def disable_reader_mode(self):
        '''
        Disable the reader mode and open up the adapter for other modes.
        '''
        self._disable_reader_mode()

    def disable_foreground_dispatch(self):
        '''
        disable foreground dispatch to the given activity.
        '''
        self._disable_foreground_dispatch(self)

    def enable_foregroung_dispatch(self):
        '''
        enable foreground dispatch to the given activity.
        '''
        self._disable_foreground_dispatch()

    def enable_foreground_ndef_push(self):
        '''
        enable foreground ndef push for NdefMessage.
        '''
        self._enable_foreground_ndef_push()

    def disable_foreground_ndef_push(self):
        '''
        disable foreground ndef push for NdefMessage.
        '''
        self._disable_foreground_ndef_push()

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

    def create_record(self, ndef_type, payload):
        '''
        Write Android NDefRecord.
        '''
        self._create_record()

    def read_record(self):
        '''
        Read Android NdefRecord.
        '''
        self._read_records()

    def create_ndef_message_bundle(self, *records):
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
        self._set_tag_mode(mode=mode)

    @property
    def tag_mode(self):
        '''
        Property that returns the mode of the tag.
            - `write`
            - `read`
        '''
        return self.get_tag_mode()

    def get_tag_mode(self):
        '''
        Get the tag mode.
        '''
        self._get_tag_mode()

    def get_tag_id(self):
        '''
        Low leve ID of the tag.
        '''
        self._get_tag_id()

    def set_message(self):
        '''
        set the message to be send.
        '''
        self._set_message()

    def get_message(self):
        '''
        get the message that is received or is created.
        '''
        self._get_message()

    def invoke_beam(self):
        '''
        manually invoke the beam.
        '''
        self._invoke_beam()

    def nfc_beam(self, files=None, ndef_message=None):
        '''
        send files through beam.
        '''
        self._nfc_beam(files=files, ndef_message=ndef_message)

    # Card Emulation

    def category_allows_foreground_preference(self, category):
        '''
        Method well documented in plyer/platform/android/nfc.py
        '''
        self._category_allows_foreground_preference(category=category)

    def get_aids_for_service(self, service, category):
        '''
        Method well documented in plyer/platform/android/nfc.py
        '''
        self._category_allows_foreground_preference(service=service,
                                                    category=category)

    def get_selection_mode_for_category(self, category):
        '''
        Method well documented in plyer/platform/android/nfc.py
        '''
        self._get_selection_mode_for_category(category=category)

    def is_default_service_for_aid(self, service, aid):
        '''
        Method well documented in plyer/platform/android/nfc.py
        '''
        self._is_default_service_for_aid(service=service, aid=aid)

    def is_default_service_for_category(self, service, category):
        '''
        Method well documented in plyer/platform/android/nfc.py
        '''
        self._is_default_service_for_category(service, category)

    def register_aids_for_service(self, service, category, aids):
        '''
        Method well documented in plyer/platform/android/nfc.py
        '''
        self._register_aids_for_service(service=service, category=category,
                                        aids=aids)

    def remove_aids_for_service(self, service, category):
        '''
        Method well documented in plyer/platform/android/nfc.py
        '''
        self._remove_aids_for_service(service=service, category=category)

    def set_preferred_service(self, activity, service):
        '''
        Method well documented in plyer/platform/android/nfc.py
        '''
        self.set_preferred_service(activity=activity, service=service)

    def unset_preferred_service(self, activity):
        '''
        Method well documented in plyer/platform/android/nfc.py
        '''
        self._unset_preferred_service(activity=activity)

    def support_aid_prefix_registration(self):
        '''
        Method well documented in plyer/platform/android/nfc.py
        '''
        self._support_aid_prefix_registration()

    # NfcF Card

    def disable_service(self, activity):
        '''
        Method well documented in plyer/platform/android/nfc.py
        '''
        self._disable_service(activity=activity)

    def enable_service(self, activity, service):
        '''
        Method well documented in plyer/platform/android/nfc.py
        '''
        self._enable_service(activity=activity, service=service)

    def set_nfcid2_for_service(self, service, nfcid2):
        '''
        Method well documented in plyer/platform/android/nfc.py
        '''
        self._set_nfcid2_for_service(service=service, nfcid2=nfcid2)

    def get_nfcid2_for_service(self, service):
        '''
        Method well documented in plyer/platform/android/nfc.py
        '''
        self._get_nfcid2_for_service(service=service)

    def get_system_code_for_service(self, service):
        '''
        Method well documented in plyer/platform/android/nfc.py
        '''
        self._get_system_code_for_service(service=service)

    def register_system_code_for_service(self, service, system_code):
        '''
        Method well documented in plyer/platform/android/nfc.py
        '''
        self._register_system_code_for_service(service=service,
                                               system_code=system_code)

    def unregister_system_code_for_service(self, service):
        '''
        Method well documented in plyer/platform/android/nfc.py
        '''
        self._unregister_system_code_for_service(service=service)

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

    def _nfc_register(self, **kwargs):
        raise NotImplementedError()

    def _enable_reader_mode(self, **kwargs):
        raise NotImplementedError()

    def _disable_reader_mode(self, **kwargs):
        raise NotImplementedError()

    def _set_tag_mode(self, **kwargs):
        raise NotImplementedError()

    def _get_tag_mode(self, **kwargs):
        raise NotImplementedError()

    def _get_tag_id(self, **kwargs):
        raise NotImplementedError()

    def _disable_foreground_dispatch(self, **kwargs):
        raise NotImplementedError()

    def _enable_foregroung_dispatch(self, **kwargs):
        raise NotImplementedError()

    def _enable_foreground_ndef_push(self, **kwargs):
        raise NotImplementedError()

    def _disable_foreground_ndef_push(self, **kwargs):
        raise NotImplementedError()

    def _enable(self, **kwargs):
        raise NotImplementedError()

    def _diable(self, **kwargs):
        raise NotImplementedError()

    def _create_record(self, **kwargs):
        raise NotImplementedError()

    def _read_record(self, **kwargs):
        raise NotImplementedError()

    def _set_message(self, **kwargs):
        raise NotImplementedError()

    def _get_message(self, **kwargs):
        raise NotImplementedError()

    def _create_ndef_message_bundle(self, *args):
        raise NotImplementedError()

    def _read_ndef_message(self, **kwargs):
        raise NotImplementedError()

    def _invoke_beam(self, **kwargs):
        raise NotImplementedError()

    def _nfc_beam(self, **kwargs):
        raise NotImplementedError()

    # Card Emulation

    def _category_allows_foreground_preference(self, **kwargs):
        raise NotImplementedError()

    def _get_aids_for_service(self, **kwargs):
        raise NotImplementedError()

    def _get_selection_mode_for_category(self, **kwargs):
        raise NotImplementedError()

    def _is_default_service_for_aid(self, **kwargs):
        raise NotImplementedError()

    def _is_default_service_for_category(self, **kwargs):
        raise NotImplementedError()

    def _register_aids_for_service(self, **kwargs):
        raise NotImplementedError()

    def _remove_aids_for_service(self, **kwargs):
        raise NotImplementedError()

    def _set_preferred_service(self, **kwargs):
        raise NotImplementedError()

    def _unset_preferred_service(self, **kwargs):
        raise NotImplementedError()

    def _support_aid_prefix_registration(self, **kwargs):
        raise NotImplementedError()

    # NfcF Card

    def _disable_service(self, **kwargs):
        raise NotImplementedError()

    def _enable_service(self, **kwargs):
        raise NotImplementedError()

    def _set_nfcid2_for_service(self, **kwargs):
        raise NotImplementedError()

    def _get_nfcid2_for_service(self, **kwargs):
        raise NotImplementedError()

    def _get_system_code_for_service(self, **kwargs):
        raise NotImplementedError()

    def _register_system_code_for_service(self, **kwargs):
        raise NotImplementedError()

    def _unregister_system_code_for_service(self, **kwargs):
        raise NotImplementedError()

    # Events for pause and resume of application.

    def _on_pause(self, **kwargs):
        raise NotImplementedError()

    def _on_resume(self, **kwargs):
        raise NotImplementedError()
