from jnius import autoclass, cast
from android.runnable import run_on_ui_thread
from android import activity
from plyer.facades import NFC

NfcAdapter = autoclass('android.nfc.NfcAdapter')
PythonActivity = autoclass('org.renpy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
IntentFilter = autoclass('android.content.IntentFilter')
PendingIntent = autoclass('android.app.PendingIntent')
BUILDVERSION = autoclass('android.os.Build$VERSION').SDK_INT
JavaString = autoclass('java.lang.String')

# Imports for Beam #
Arraylist = autoclass('java.util.ArrayList')
Uri = autoclass('android.net.Uri')
File = autoclass('java.io.File')
# End Beam imports
NdefRecord = autoclass('android.nfc.NdefRecord')
NdefMessage = autoclass('android.nfc.NdefMessage')
Tag = autoclass('android.nfc.Tag')
# Tech imports.
IsoDep = autoclass('android.nfc.tech.IsoDep')
MifareClassic = autoclass('android.nfc.tech.MifareClassic')
MifareUltralight = autoclass('android.nfc.tech.MifareUltralight')
Ndef = autoclass('android.nfc.tech.Ndef')
NdefFormatable = autoclass('android.nfc.tech.NdefFormatable')
NfcA = autoclass('android.nfc.tech.NfcA')
NfcB = autoclass('android.nfc.tect.NfcB')
NfcF = autoclass('android.nfc.tech.NfcF')
NfcV = autoclass('android.nfc.tech.NfcV')
NfcBarcode = autoclass('android.nfc.tech.NfcBarcode')

NfcManager = autoclass('android.nfc.NfcManager')
# Used to obtain an instance instance of NfcAdapter.
NfcEvent = autoclass('android.nfc.NfcEvent')
# Information associated with NFC events

# Card Emulation imports.
CardEmulation = autoclass('android.nfc.cardemulation.CardEmulation')
NfcFCardEmulation = autoclass('android.nfc.cardemulation.NfcFCardEmulation')


class PyNdefRecord(NFC.NdefRecord):
    '''
    This class is to hide the details of how the NDefRecord is created.
    User just needs to pass the payload and the ndef_type after creating
    an instance and pass the expected parameters while calling the instance.
    '''

    def __call__(self, **kwargs):
        '''
        Method that returns different type of record depending upon
        the ndef_type given.
        '''

        payload = kwargs.get("payload")
        # Dictionary type
        ndef_type = kwargs.get("ndef_type")
        # String type

        if ndef_type == "application":
            return self._create_application_record(payload)
        elif ndef_type == "external":
            return self._create_external(payload)
        elif ndef_type == "mime":
            return self._create_mime(payload)
        elif ndef_type == "text_record":
            return self._create_text_record(payload)
        elif ndef_type == "uri":
            return self._create_uri(payload)
        elif ndef_type == 'custom':
            return self._create_custom_record(payload)
        elif ndef_type == "alternative_carrier":
            return self._create_RTD_ALTERNATIVE_CARRIER(payload)
        elif ndef_type == "handover_carrier":
            return self._create_uri(payload)
        elif ndef_type == "handover_request":
            return self._create_uri(payload)
        elif ndef_type == "handover_select":
            return self._create_uri(payload)
        elif ndef_type == "smart_poster":
            return self._create_uri(payload)
        elif ndef_type == "text":
            return self._create_RTD_TEXT(payload)
        else:
            return False

    def _create_application_record(self, **kwargs):
        '''
        Creates a record of type application record.

        Expects 1 parameters in kwargs.:
            - payload: Dict type
                - package_name: String: Application package name.

        returns a NDefRecord type
        '''
        payload = kwargs.get('payload')
        package_name = payload.get('package_name')
        record = NdefRecord.createApplicationRecord(JavaString(package_name))
        return record

    def _create_external(self, **kwargs):
        '''
        Creates a record of type external.
        Expects 1 parameters in the kwargs.
            - payload: Dict type
                - domain: String: domain-name of the issuing organisation.
                - external_type: String: domain-specific type of data.
                - data: Byte: payload as bytes.

        returns a NDefRecord type.
        '''
        payload = kwargs.get('payload')
        domain = payload.get('domain')
        external_type = payload.get('external_type')
        data = kwargs.get('data')
        if BUILDVERSION > 16:
            try:
                return NdefRecord.createExternal(JavaString(domain),
                                                 JavaString(external_type),
                                                 data)
            except:
                raise Exception('Either domain or type are empty or invaild.')
        record = NdefRecord(NdefRecord.TNF_EXTERNAL_TYPE,
                            "{} + ':' + {}".format(JavaString(domain),
                                                   JavaString(external_type)),
                            '',
                            payload)
        try:
            return record
        except:
            raise Exception('Either domain or type are empty or invaild.')

    def _create_mime(self, **kwargs):
        '''
        Creates a record that contains a MIME type.
        Expects 1 parameter in the kwargs.
            - payload: Dict type
                - mime_type: String: a valid MIME type.
                - mime_data: Byte: MIME data in bytes.

        returns a NDefRecord type.
        '''
        payload = kwargs.get('payload')
        mime_type = payload.get('mime_type')
        mime_data = payload.get('mime_data')
        if BUILDVERSION > 16:
            return NdefRecord.createMime(JavaString(mime_type),
                                         mime_data)
        record = NdefRecord(NdefRecord.TNF_MIME_MEDIA,
                            JavaString(mime_type),
                            '',
                            mime_data)
        return record

    def _create_text_record(self, **kwargs):
        '''
        Creates a record that contains a URF-8 text data.
        Expects 1 parameters in the kwargs.
            - payload: Dict type.
                - language_code: String:
                - text: String: The text to be encoded.

        returns a NDefRecord type.
        '''
        payload = kwargs.get('payload')
        language_code = payload.get('language_code')
        text = kwargs.get('text')
        if BUILDVERSION > 21:
            try:
                return NdefRecord.createTextRecord(JavaString(language_code),
                                                   JavaString(text))
            except:
                raise Exception('Either MIME type is empty or invalid.')
        record = NdefRecord(NdefRecord.TNF_WELL_KNOWN,
                            language_code,
                            '',
                            text)
        try:
            return record
        except:
            raise Exception('Either MIME type is empty or invalid.')

    def _create_uri(self, **kwargs):
        '''
        Creates a record that contains a uri.
        Expects 1 parameters in the kwargs.
            - payload: Dict type.
                - uri: String/ uri:

        returns a NDefRecord type.
        '''
        payload = kwargs.get('payload')
        uri = payload.get('uri')
        if BUILDVERSION > 14:
            try:
                return NdefRecord.createUri(JavaString(uri))
            except:
                try:
                    return NdefRecord.createUri(uri)
                except:
                    raise Exception('Either uri is empty or invalid.')

        record = NdefRecord(NdefRecord.TNF_WELL_KNOWN,
                            NdefRecord.RTD_URI,
                            '',
                            uri)
        try:
            return record
        except:
            raise Exception('Either uri is empty or invalid.')

    def _create_custom_record(self, **kwargs):
        '''
        Create a record of the parameters that you pass to it.
        This is a standard API and expects everything for user.
        Including the TNF and RTD types.

        Expects 1 parameter in the kwargs:
            - payload: Dict type.
                - tnf: Short: e.g; NDefRecord.TNF_*_* type
                - record_type: byte: example; NDefRecord.RTD_*_* type
                - record_id: byte: id in bytes.
                - payload: byte: data in bytes.

        returns a NdefRecord type.
        '''
        payload = kwargs.get('payload')
        tnf = payload.get('tnf')
        record_type = payload.get('record_type')
        record_id = payload.get('record_id')
        data = payload.get('payload')

        record = NdefRecord(tnf,
                            record_type,
                            record_id,
                            data)

        try:
            return record
        except:
            raise Exception('Either data is empty or Invalid.')

    def _create_RTD_ALTERNATIVE_CARRIER(self, **kwargs):
        '''
        Creates a record for RTD_ALTERNATIVE_CARRIER.
        Expects 1 parameters in the kwargs.
            - payload: Dict type.
                - data: bytes:

        returns a NDefRecord type.
        '''
        payload = kwargs.get('payload')
        data = payload.get('alterative_carrier')
        record = NdefRecord(NdefRecord.TNF_WELL_KNOWN,
                            NdefRecord.RTD_ALTERNATIVE_CARRIER,
                            '',
                            data)
        return record

    def _create_RTD_HANDOVER_CARRIER(self, **kwargs):
        '''
        Creates a record for RTD_HANDOVER_CARRIER.
        Expects 1 parameters in the kwargs.
            - payload: Dict type.
                - data: bytes:

        returns a NDefRecord type.
        '''
        payload = kwargs.get('payload')
        data = payload.get('handover_carrier')
        record = NdefRecord(NdefRecord.TNF_WELL_KNOWN,
                            NdefRecord.RTD_HANDOVER_CARRIER,
                            '',
                            data)
        return record

    def _create_RTD_HANDOVER_REQUEST(self, **kwargs):
        '''
        Creates a record for RTD_HANDOVER_REQUEST.
        Expects 1 parameters in the kwargs.
            - payload: Dict type.
                - data: bytes:

        returns a NDefRecord type.
        '''
        payload = kwargs.get('payload')
        data = payload.get('handover_request')
        record = NdefRecord(NdefRecord.TNF_WELL_KNOWN,
                            NdefRecord.RTD_HANDOVER_REQUEST,
                            '',
                            data)
        return record

    def _create_RTD_HANDOVER_SELECT(self, **kwargs):
        '''
        Creates a record for RTD_HANDOVER_SELECT.
        Expects 1 parameters in the kwargs.
            - payload: Dict type.
                - data: bytes:

        returns a NDefRecord type.
        '''
        payload = kwargs.get('payload')
        data = payload.get('handover_select')
        record = NdefRecord(NdefRecord.TNF_WELL_KNOWN,
                            NdefRecord.RTD_HANDOVER_SELECT,
                            '',
                            data)
        return record

    def _create_RTD_SMART_POSTER(self, **kwargs):
        '''
        Creates a record for RTD_SMART_POSTER.
        Expects 1 parameters in the kwargs.
            - payload: Dict type.
                - data: bytes:

        returns a NDefRecord type.
        '''
        payload = kwargs.get('payload')
        data = payload.get('smart_poster')
        record = NdefRecord(NdefRecord.TNF_WELL_KNOWN,
                            NdefRecord.RTD_SMART_POSTER,
                            '',
                            data)
        return record

    def _create_RTD_TEXT(self, **kwargs):
        '''
        Creates a record for RTD_TEXT.
        Expects 1 parameters in the kwargs.
            - payload: Dict type.
                - data: bytes:

        returns a NDefRecord type.
        '''
        payload = kwargs.get('payload')
        data = payload.get('text')
        record = NdefRecord(NdefRecord.TNF_WELL_KNOWN,
                            NdefRecord.RTD_TEXT,
                            '',
                            data)
        return record


class AndroidNFC(NFC):

    '''
    some methods adapted from
    `https://gist.github.com/tito/9e2308a4c942ddb2342b`
    and
    `https://gist.github.com/akshayaurora/b76dbcc69c9850bb3e318af4722a0b4f`

    some methods inspired from
    `https://developer.android.com/reference/android/nfc/package-summary.html`
    '''
    def _nfc_register(self, **kwargs):
        '''
        Initializing NFC adapter and listing the techs available.
        Expects three parameters.
            action_list: dict
                {ndef, tech, tag, card, f-card}
            tech_list: dict
                {all, IsoDep, NfcA, NfcB, NfcF, NfcV, Ndef, NfcBarcode,
                 NdefFormattable, Mifareclassic, MifareUltralight}
            data_type: String
                'text/plain'
                'image/jpeg'
                'image/*'
                '*/*'
                etc...
        '''
        self.j_context = context = PythonActivity.mActivity
        self.nfc_adapter = NfcAdapter.getDefaultAdapter(context)
        if not nfc_adapter:
            raise Exception('No adapter found.')

        self.nfc_pending_intent = PendingIntent.getActivity(
            context, 0,
            Intent(context, context.getClass()).addFlags(
                Intent.FLAG_ACTIVITY_SINGLE_TOP), 0)

        self.tech_list = kwargs.get('tech_list')
        self.action_list = kwargs.get('action_list')
        self.data_type = kwargs.get('data_type')

        self.message = None
        self.tag_mode = 'read'
        self.tag_id = None

        self.ndef_exchange_filters = []
        if 'ndef' in action_list:
            self.ndef_detected = IntentFilter(
                NfcAdapter.ACTION_NDEF_DISCOVERED)
            self.ndef_detected.addDataType(self.data_type)
            self.ndef_exchange_filters.append(self.ndef_detected)

        if 'tech' in action_list:
            self.tech_detected = IntentFilter(
                NfcAdapter.ACTION_TECH_DISCOVERED)
            self.tech_detected.addDataType(self.data_type)
            self.ndef_exchange_filters.append(self.tech_detected)

        if 'tag' in action_list:
            self.tag_detected = IntentFilter(
                NfcAdapter.ACTION_TAG_DISCOVERED)
            self.tag_detected.addDataType(self.data_type)
            self.ndef_exchange_filters.append(self.tag_detected)

        if 'card' in action_list:
            self.card = NfcFCardEmulation.getInstance(self.nfc_adapter)

        if 'f-card' in action_list:
            self.nfcf_card = NfcFCardEmulation.getInstance(self.nfc_adapter)

        self.ndef_tech_list = []

        if 'all' in self.tech_list:
            self.ndef_tech_list = [
                ['android.nfc.tech.IsoDep'],
                ['android.nfc.tech.NfcA'],
                ['android.nfc.tech.NfcB'],
                ['android.nfc.tech.NfcF'],
                ['android.nfc.tech.NfcV'],
                ['android.nfc.tech.Ndef'],
                ['android.nfc.tech.NfcBarcode'],
                ['android.nfc.tech.NdefFormattable'],
                ['android.nfc.tech.MifareClassic'],
                ['android.nfc.tech.MifareUltralight']]

        else:
            for tech in self.tech_list:
                self.ndef_tech_list.append(
                    ['android.nfc.tech.{}'.format(tech)])

        self._enable()
        self._on_new_intent(PythonActivity.getIntent())
        return True

    def _enable_reader_mode(self):
        '''
        Limit the NFC controller to reader mode while this Activity is in the
        foreground.
        '''
        self.nfc_adapter.enableReaderMode(self.j_context,
                                          callback,
                                          flags,
                                          extras)

    def _disable_reader_mode(self):
        '''
        Restore the NFC adapter to normal mode of operation: supporting
        peer-to-peer (Android Beam),
        card emulation, and
        polling for all supported tag technologies.
        '''
        self.nfc_adapter.disableReaderMode(self.j_context)

    @run_on_ui_thread
    def _disable_foreground_dispatch(self):
        '''
        disable foreground dispatch to the given activity.
        '''
        self.nfc_adapter.disableForegroundDispatch(self.j_context)

    @run_on_ui_thread
    def _enable_foreground_dispatch(self):
        '''
        Enable foreground dispatch to the given activity.
        '''
        self.nfc_adapter.enableForegroundDispatch(self.j_context,
                                                  self.nfc_pending_intent,
                                                  self.ndef_exchange_filters,
                                                  self.ndef_tech_list)

    @run_on_ui_thread
    def _enable_foreground_ndef_push(self):
        '''
        NOTE: This method was deprecated in API level 14.
        please use `set_ndef_push_message`.

        enable foreground ndef push for message to be send via android beam.
        '''
        self.nfc_adapter.enableForegroundNdefPush(self.j_context, self.message)

    @run_on_ui_thread
    def _disable_foreground_ndef_push(self):
        '''
        NOTE: This method was deprecated in API level 14.
        please use `set_ndef_push_message`.

        disable foreground dispatch to be send using Android Beam.
        '''
        self.nfc_adapter.disableForegroundNdefPush(self.j_context)

    def _on_new_intent(self, intent):
        '''
        This method is called for activities that set launchMode to "singleTop"
        in their package, or if a client used the FLAG_ACTIVITY_SINGLE_TOP flag
        when calling startActivity(Intent).
        As done when passing pending intent(self.nfc_pending_intent)to the
        `enableForeGroundDispatch` method.
        '''
        if intent.getAction() == NfcAdapter.ACTION_NDEF_DISCOVERED:

            try:
                extra_msgs = intent.getParcelableArrayExtra(
                                    NfcAdapter.EXTRA_NDEF_MESSAGES)
                # An array of NDEF messages parsed from the tag.
                if extra_msgs:
                    self.message = extra_msgs

                extra_tag = intent.getParcelableExtra(NfcAdapter.EXTRA_TAG)
                if extra_tag:
                    self._handle_tag(intent)
                # Tag object representing the scanned tag.
                extra_ID = intent.getParcelableExtra(NfcAdapter.EXTRA_ID)
                if extra_ID:
                    self.tag_id = extra_ID
                # Low Level ID of the tag

        elif intent.getAction() == NfcAdapter.ACTION_TECH_DISCOVERED:
            return

        elif intent.getAction() == NfcAdapter.ACTION_TAG_DISCOVERED:
            # If tag is discovered.
            self._handle_tag(intent)

    def _disable(self):
        '''
        Dissable the foreground dispatch and unbind the activity from
        `on_new_intent` method.
        '''
        activity.unbind(on_new_intent=self._on_new_intent)
        self._disable_foreground_dispatch()

    def _enable(self):
        '''
        Enable the foreground dispatch and bind the activity with the
        `on_new_intent` method in case some action in triggered.
        '''
        activity.bind(on_new_intent=self._on_new_intent)
        self._enable_foreground_dispatch()

    def _create_record(self, ndef_type, payload):
        '''
        Expects 2 parameters:
            - ndef_type: String
            - payload: dict
        For writing android NdefRecords.

        Returns a NdefRecord type.
        '''
        record = PyNdefRecord()
        return record(ndef_type, payload)

    def _read_record(self, **kwargs):
        '''
        Expects 1 parameter:
            - record: NDefRecord type.
        Reading android NdefRecords.

        retutns the payload form the record.
        '''
        record = kwargs.get('record')
        payload = record.getPayload()
        return payload

    # ------------------------
    # Setters and Getters
    # ------------------------

    def _set_tag_mode(self, **kwargs):
        '''
        Set the Tag mode from two choices.
        Read and right.
        '''
        mode = kwargs.get('mode')
        self.tag_mode = mode

    def _get_tag_mode(self):
        '''
        Get the tag mode.
        '''
        return self.tag_mode

    def _get_tag_id(self):
        '''
        Low level ID of the tag
        '''
        return self.tag_id

    def _set_message(self, **kwargs):
        '''
        Expects 1 parameter:
            - message: NDefMesage type.

        '''
        msg = kwargs.get('message')
        self.message = msg

    def _get_message(self):
        '''
        Returns the tag message which is stored either manually by
        `set_message` method. OR
        when the `ACTION_TAG_DISCOVERED` writes to the tag_messsage.
        '''
        return self.message

    def _read_ndef_message(self, **kwargs):
        '''
        Expects 1 parameter:
            - messages: NDefMessage type
                - record: NDefRecord type
                - record: NDefRecord type
                - ....
        Reading android NdefMessage.
        '''
        messages = kwargs.get('messages')
        if not messages:
            return

        for message in messages:
            message = cast(NdefMessage, message)
            payload = message.getRecords()[0].getPayload()
        return payload

    def _create_ndef_message_bundle(self, *records):
        '''
        Expects a list of records so they could be put in a
        NdefMessage and used by other NFC features.
        NdefMessage that will be written on tag.

        returns NDefMessage type.
        '''
        return NdefMessage([record for record in records if record])

    # -------------------
    # P2P
    # -------------------

    def _invoke_beam(self):
        '''
        Manually invoke android beam to share data.
        '''
        self.nfc_adapter.invokeBeam(self.j_context)

    def _nfc_beam(self, **kwargs):
        try:
            files = kwargs.get('files')
            if files:
                filesUris = Arraylist()
                for i in range(len(files)):
                    share_file = File(files[i])
                    uri = Uri.fromFile(share_file)
                    filesUris.add(uri)

                self.nfc_adapter.setBeamPushUris(filesUris, self.j_context)
            ndef_message = kwargs.get('ndef_message')
            if ndef_message:
                self.nfc_adapter.setNdefPushMessage(ndef_message,
                                                    self.j_context)
        except:
            return False

    # -----------------------------
    # TAG reading and writing.
    # -----------------------------

    def _handle_tag(self, intent):
        '''
        Reading the tags of the type listed in the ndef_tech_list.
        '''

        extre_tag = intent.getParcableExtra(NfcAdapter.EXTRA_TAG)
        tag = cast('android.nfc.Tag', extra_tag)
        taglist = tag.getTechList()

        for i in range(len(taglist)):

            if taglist[i] == MifareClassic.class.getName():
                mctag = MifareClassic.get(tag)

                if self.tag_mode == 'read':
                    self._read_classic_tag()
                elif self.tag_mode == 'write':
                    self._write_classic_tag(tag, details)
                else:
                    raise ValueError('Wrong tag mode given, ' +
                                     'modes: `read` or `write`)')

            elif taglist[i] == MifareUltralight.class.getName():
                if sef.tag_mode == 'read':
                    self._read_ultra_tag(tag)
                elif self.tag_mode == 'write':
                    self._write_ultra_tag(tag, details)
                else:
                    raise ValueError('Wrong tag mode given, ' +
                                     'modes: `read` or `write`)')

            elif taglist[i] == IsoDep.class.getName():
                if self.tag_mode == 'read':
                    self._read_isodep_rag(tag)
                elif self.tag_mode == 'write':
                    self._write_isodep_tag(tag, details)
                else:
                    raise ValueError('Wrong tag mode given, ' +
                                     'modes: `read` or `write`)')

            elif taglist[i] == Ndef.class.getName():
                if self.tag_mode == 'read':
                    self._read_ndef_tag(tag)
                elif self.tag_mode == 'write':
                    self._write_ndef_tag(tag, details)
                else:
                    raise ValueError('Wrong tag mode given, ' +
                                     'modes: `read` or `write`)')

            elif taglist[i] == NdefFormatable.class.getName():
                if self.tag_mode == 'read':
                    raise Exception("Can't write for this format")
                elif self.tag_mode == 'write':
                    self._write_ndef_formattable_tag(tag, details)
                else:
                    raise ValueError('Wrong tag mode given, ' +
                                     'modes: `read` or `write`)')

            elif taglist[i] == NfcA.class.getName():
                if self.tag_mode == 'read':
                    self._read_ndef_formattable_tag(tag)
                elif self.tag_mode == 'write':
                    self._write_ndef_formattable_tag(tag, details)
                else:
                    raise ValueError('Wrong tag mode given, ' +
                                     'modes: `read` or `write`)')

            elif taglist[i] == NfcB.class.getName():
                if self.tag_mode == 'read':
                    self._read_ndef_formattable_tag(tag)
                elif self.tag_mode == 'write':
                    self._write_ndef_formattable_tag(tag, details)
                else:
                    raise ValueError('Wrong tag mode given, ' +
                                     'modes: `read` or `write`)')

            elif taglist[i] == NfcF.class.getName():
                if self.tag_mode == 'read':
                    self._read_ndef_formattable_tag(tag)
                elif self.tag_mode == 'write':
                    self._write_ndef_formattable_tag(tag, details)
                else:
                    raise ValueError('Wrong tag mode given, ' +
                                     'modes: `read` or `write`)')

            elif taglist[i] == NcfV.class.getName():
                if self.tag_mode == 'read':
                    self._read_ndef_formattable_tag(tag)
                elif self.tag_mode == 'write':
                    self._write_ndef_formattable_tag(tag, details)
                else:
                    raise ValueError('Wrong tag mode given, ' +
                                     'modes: `read` or `write`)')

            elif taglist[i] == NfcBarcode.class.getName():
                if self.tag_mode == 'read':
                    self._read_nfc_barcode_tag()
                elif self.tag_mode == 'write':
                    raise Exception('Writing this tag is not possible.')
                else:
                    raise ValueError('Wrong tag mode given, ' +
                                     'modes: `read` or `write`)')

            else:
                raise Exception('Unknown Tag found.')

    # Reading Tags.

    def _read_classic_tag(self, Tag):
        '''
        Expects 1 parameters.
            tag: Tag type.

        This method is called when `ACTION_TAG_DISCOVERED` happens and tag_mode
        is set to `read` and the tag type is MifareClassic.
        '''
        tech_tag = cast('android.nfc.tech.MifareClassic',
                        MifareClassic.get(tag))
        details = {}
        try:
            tech_tag.connect()
            details['BlockCount'] = tech_tag.getBlockCount()
            details['BlockCountInSector'] = tech_tag.getBlockCountInSector()
            details['MaxTransceiveLength'] = tech_tag.getMaxTransceiveLength()
            details['SectorCount'] = tech_tag.getSectorCount()
            details['Size'] = tech_tag.getSize()
            details['TimeOut'] = tech_tag.getTimeOut()
            details['Type'] = tech_tag.getType()
            details['Block'] = tech_tag.readBlock()
            tech_tag.close()
        except:
            raise Exception('Either Tag is lost or I/O failure.')
        finally:
            # return details
            self._set_message(details)

    def _read_ultra_tag(self, Tag):
        '''
        Expects 1 parameters.
            tag: Tag type.

        This method is called when `ACTION_TAG_DISCOVERED` happens and tag_mode
        is set to `read` and the tag type is MifareUltralight.
        '''
        tech_tag = cast('android.nfc.tech.MifareUltralight',
                        MifareUltralight.get(tag))
        details = {}
        payload = {}
        try:
            tech_tag.connect()
            details['Type'] = tech_tag.getType()
            details['MaxTransceiveLength'] = tech_tag.getMaxTransceiveLength()
            for i in range(1, 17):
                payload['{}'.format(i)] = tech_tag.readPages(i)
            details['pages'] = payload
            tech_tag.close()
        except:
            raise Exception('Either Tag is lost or I/O failure.')
        finally:
            self._set_message(details)

    def _read_iso_dep_tag(self, tag):
        '''
        Expects 1 parameters.
            tag: Tag type.

        This method is called when `ACTION_TAG_DISCOVERED` happens and tag_mode
        is set to `read` and the tag type is IsoDep.
        '''
        tech_tag = cast('android.nfc.tech.IsoDep', IsoDep.get(tag))
        details = {}
        try:
            tech_tag.connect()
            details['HiLayerResponse'] = tech_tag.getHiLayerResponse()
            details['HistoricalBytes'] = tech_tag.getHistoricalBytes()
            details['MaxTransceiveLength'] = tech_tag.getMaxTransceiveLength()
            details['TimeOut'] = tech_tag.getTimeOut()
            details['isExtendedLengthApduSupported'] = \
                tech_tag.isExtendedLengthApduSupported()
            tech_tag.close()
        except:
            raise Exception('Either Tag is lost or I/O failure.')
        finally:
            self._set_message(details)

    def _read_ndef_tag(self, tag):
        '''
        Expects 1 parameters.
            tag: Tag type.

        This method is called when `ACTION_TAG_DISCOVERED` happens and tag_mode
        is set to `read` and the tag type is Ndef.
        '''
        tech_tag = cast('android.nfc.tech.Ndef', Ndef.get(tag))
        details = {}
        try:
            tech_tag.connect()
            details['MaxSize'] = tech_tag.getMaxSize()
            details['writable'] = tech_tag.isWritable()
            details['Readonly'] = tech_tag.canMakeReadOnly()

            ndefMesg = tech_tag.getCachedNdefMessage()
            details['Type'] = tech_tag.getType()
            if not ndefMesg:
                details['Message'] = None
                return details

            ndefrecords = ndefMesg.getRecords()
            recTypes = []
            for record in ndefrecords:
                recTypes.append({
                    'type': ''.join(map(chr, record.getType())),
                    'payload': ''.join(map(chr, record.getPayload()))})

            details['recTypes'] = recTypes
            tech_tag.close()
        except:
            raise Exception('Either Tag is lost or I/O failure.')
        finally:
            self._set_message(details)

    def _read_nfcA_tag(self, tag):
        '''
        Expects 1 parameters.
            tag: Tag type.

        This method is called when `ACTION_TAG_DISCOVERED` happens and tag_mode
        is set to `read` and the tag type is NfcA.
        '''
        tech_tag = cast('android.nfc.tech.NfcA', NfcA.get(tag))
        details = {}
        try:
            tech_tag.connect()
            details['Atqa'] = tech_tag.getAtqa()
            details['MaxTransceiveLength'] = tech_tag.getMaxTransceiveLength()
            details['Sak'] = tech_tag.getSak()
            details['TimeOut'] = tech_tag.getTimeOut()
            tech_tag.close()
        except:
            raise Exception('Either Tag is lost or I/O failure.')
        finally:
            self._set_message(details)

    def _read_nfcB_tag(self, tag):
        '''
        Expects 1 parameters.
            tag: Tag type.

        This method is called when `ACTION_TAG_DISCOVERED` happens and tag_mode
        is set to `read` and the tag type is NfcB.
        '''
        tech_tag = cast('android.nfc.tech.NfcB', NfcB.get(tag))
        details = {}
        try:
            tech_tag.connect()
            details['ApplicationData'] = tech_tag.getApplicationData()
            details['MaxTransceiveLength'] = tech_tag.getMaxTransceiveLength()
            details['ProtocolInfo'] = tech_tag.getProtocolInfo()
            tech_tag.close()
        except:
            raise Exception('Either Tag is lost or I/O failure.')
        finally:
            self._set_message(details)

    def _read_nfcF_tag(self, tag):
        '''
        Expects 1 parameters.
            tag: Tag type.

        This method is called when `ACTION_TAG_DISCOVERED` happens and tag_mode
        is set to `read` and the tag type is NfcF.
        '''
        tech_tag = cast('android.nfc.tech.NfcF', NfcF.get(tag))
        details = {}
        try:
            tech_tag.connect()
            details['Manufacturer'] = tech_tag.getManufacturer()
            details['MaxTransceiveLength'] = tech_tag.getMaxTransceiveLength()
            details['SystemCode'] = tech_tag.getSystemCode()
            details['TimeOut'] = tech_tag.getTimeOut()
            tech_tag.close()
        except:
            raise Exception('Either Tag is lost or I/O failure.')
        finally:
            self._set_message(details)

    def _read_nfcV_tag(self, tag):
        '''
        Expects 1 parameters.
            tag: Tag type.

        This method is called when `ACTION_TAG_DISCOVERED` happens and tag_mode
        is set to `read` and the tag type is NfcV.
        '''
        tech_tag = cast('android.nfc.tech.NfcV', NfcV.get(tag))
        details = {}
        try:
            tech_tag.connect()
            details['DsfId'] = tech_tag.getDsfId()
            details['MaxTransceiveLength'] = tech_tag.getMaxTransceiveLength()
            details['ResponseFlags'] = tech_tag.getResponseFlags()
            tech_tag.close()
        except:
            raise Exception('Either Tag is lost or I/O failure.')
        finally:
            self._set_message(details)

    def _read_nfc_barcode_tag(self, tag):
        '''
        Expects 1 parameters.
            tag: Tag type.

        This method is called when `ACTION_TAG_DISCOVERED` happens and tag_mode
        is set to `read` and the tag type is NfcBarcode.
        '''
        tech_tag = cast('android.nfc.tech.NfcBarcode', NfcBarcode.get(tag))
        details = {}
        try:
            tech_tag.connect()
            details['Type'] = tech_tag.getType()
            details['Barcode'] = tech_tag.getBarcode()
            tech_tag.close()
        except:
            raise Exception('Either Tag is lost or I/O failure.')
        finally:
            self._set_message(details)

    # Writing Tags.

    def _write_classic_tag(self, tag, details):
        '''
        Expects two parameters.
            tag: Tag
            details: dict
                blockIndex: int
                timeout: int
                data: byte
                transceive: boolean

        This method is called when `ACTION_TAG_DISCOVERED` happens and tag_mode
        is set to be `write` and the tag type is MifareClassic.
        '''
        tech_tag = cast('android.nfc.tech.MifareClassic',
                        Mifareclassic.get(tag))
        try:
            tech_tag.connect()
            block_index = details['blockIndex']
            data = details['data']
            if details['transceive']:
                tech_tag.transceive(data)
            timeout = details['timeout']
            if timeout:
                tech_tag.setTimeout(timeout)
            if blockIndex:
                if data:
                    tech_tag.writeBlock(blockIndex, data)
            tech_tag.close()
        except:
            raise Exception('Unable to write tag')

    def _write_ultra_tag(self, tag, details):
        '''
        Expects two parameters.
            tag: Tag
            details: dict
                timeout: int
                transceive: boolean
                data: byte
                pageOffset: int

        This method is called when `ACTION_TAG_DISCOVERED` happens and
        tag_mode is set to be `write` and the tag type is MifareUltralight.
        '''
        tech_tag = cast('android.nfc.tech.MifareUltralight',
                        MifareUltralight.get(tag))
        try:
            tech_tag.connect()
            timeout = details['timeout']
            if timeout:
                tech_tag.setTimeout(timeout)
            data = details['data']
            if details['transceive']:
                tech_tag.transceive(data)
            page_off_set = details['pageOffset']
            if page_off_set:
                tech_tag.writePage(page_off_set, data)
            tech_tag.close()
        except:
            raise Exception('unable to write tag.')

    def _write_isodep_tag(self, tag, details):
        '''
        Expects two parameters.
            tag: Tag type.
            details: dict type
                timeout: int
                data: byte
                transceive: boolean

        This method is called when `ACTION_TAG_DISCOVERED` happens and tag_mode
        is set to be `write` and the tag type is IsoDep.
        '''
        tech_tag = cast('android.nfc.tech.IsoDep', IsoDep.get(tag))
        try:
            tech_tag.connect()
            timeout = details['timeout']
            if timeout:
                tech_tag.setTimeout(timeout)
            transceive = details['transceive']
            data = details['data']
            if transceive:
                tech_tag.transceive(data)
            tech_tag.close()
        except:
            raise Exception('Unable to write tag')

    def _write_ndef_tag(self, tag, details):
        '''
        Expects two parameters.
            tag: Tag
            details: dict
                makeReadOnly: boolean
                ndef_message: NdefMessage

        This method is called when `ACTION_TAG_DISCOVERED` happens and tag_mode
        is set to be `write` and the tag type is Ndef.
        '''
        tech_tag = cast('android.nfc.tech.Ndef', Ndef.get(tag))
        try:
            tech_tag.connect()
            if details['makeReadOnly']:
                tech_tag.makeReadOnly()
            ndef_message = details['ndef_message']
            tech_tag.writeNdefMessage(ndef_message)
            tech_tag.close()
        except:
            raise Exception('Unable to write tag')

    def _write_ndef_formattable_tag(self, tag, details):
        '''
        Expects two parameters.
            tag: Tag type.
            details: dict type
                format: boolean
                formatReadOnly: boolean
                ndef_message: NdefMessage

        This method is called when `ACTION_TAG_DISCOVERED` happens and tag_mode
        is set to be `write` and the tag type is NdefFormattable.
        '''
        tech_tag = cast('android.nfc.tech.NdefFormatable',
                        NdefFormatable.get(tag))
        try:
            tech_tag.connect()
            ndef_message = details['ndef_message']
            if details['format']:
                tech_tag.format(ndef_message)
            if details['formatReadOnly']:
                tech_tag.formatReadOnly(ndef_message)
            tech_tag.close()
        except:
            raise Exception('Unable to write tag')

    def _write_nfcA_tag(self, tag, details):
        '''
        Expects two parameters.
            tag: Tag type.
            details: dict type
                data: byte
                timeout: int
                transceive: boolean

        This method is called when `ACTION_TAG_DISCOVERED` happens and tag_mode
        is set to be `write` and the tag type is NfcA.
        '''
        tech_tag = cast('android.nfc.tech.NfcA', NfcA.get(tag))
        try:
            tech_tag.connect()
            timeout = details['timeout']
            if timeout:
                tech_tag.setTimeout(timeout)
            transceive = details['transceive']
            data = details['data']
            if transceive:
                tech_tag.transceive(data)
            tech_tag.close()
        except:
            raise Exception('Unable to write tag')

    def _write_nfcB_tag(self, tag, details):
        '''
        Expects two parameters.
            tag: Tag type.
            details: dict type
                data: byte
                transceive: boolean

        This method is called when `ACTION_TAG_DISCOVERED` happens and tag_mode
        is set to be `write` and the tag type is NfcB.
        '''
        tech_tag = cast('android.nfc.tech.NfcB', NfcB.get(tag))
        try:
            tech_tag.connect()
            transceive = details['transceive']
            data = details['data']
            if transceive:
                tech_tag.transceive(data)
            tech_tag.close()
        except:
            raise Exception('Unable to write tag')

    def _write_nfcF_tag(self, tag, details):
        '''
        Expects two parameters.
            tag: Tag type.
            details: dict type
                data: byte
                timeout: int
                transceive: boolean

        This method is called when `ACTION_TAG_DISCOVERED` happens and tag_mode
        is set to be `write` and the tag type is NfcF
        '''
        tech_tag = cast('android.nfc.tech.NfcF', NfcF.get(tag))
        try:
            tech_tag.connect()
            timeout = details['timeout']
            if timeout:
                tech_tag.setTimeout(timeout)
            transceive = details['transceive']
            data = details['data']
            if transceive:
                tech_tag.transceive(data)
            tech_tag.close()
        except:
            raise Exception('Unable to write tag')

    def _write_nfcV_tag(self, tag, details):
        '''
        Expects two parameters.
            tag: Tag type.
            details: dict type
                data: byte
                transceive: boolean

        This method is called when `ACTION_TAG_DISCOVERED` happens and tag_mode
        is set to be `write` and the tag type is NfcV.
        '''
        tech_tag = cast('android.nfc.tech.NfcV', NfcV.get(tag))
        try:
            tech_tag.connect()
            transceive = details['transceive']
            data = details['data']
            if transceive:
                tech_tag.transceive(data)
            tech_tag.close()
        except:
            raise Exception('Unable to write tag')

    # card emulation part.

    # -------------------------------------------
    # Reference API for CardEmulation class.
    # -------------------------------------------

    def _category_allows_foreground_preference(self, **kwargs):
        '''
        Expects 1 parameters:

            - category: String, e.g: CATEGORY_PAYMENT

        Returns whether the user has allowed AIDs registered in the specified
        category to be handled by a service that is preferred by the foreground
        application, instead of by a pre-configured default.
        To set preferences use `_set_preferred_service` method.

        returns boolean value.
        '''
        category = kwargs.get('category')
        return self.card.categoryAllowsForegroundPreference(category)

    def _get_aids_for_service(self, **kwargs):
        '''
        Expects 2 parameters:
            - services: componentName
            - category: String, e.g CATEGORY_PAYMENT

        Retrieves the currently registered AIDs for the specified category
        for a service.
        '''
        service = kwargs.get('service')
        category = kwargs.get('category')
        return self.card.getAidsForService(service, category)

    def _get_selection_mode_for_category(self, **kwargs):
        '''
        Expects 1 parameters:
            - category: String, e.g: CATEGORY_PAYMENT

        Returns the service selection mode for the passed in category.
        Valid return values are:
            - SELECTION_MODE_PREFER_DEFAULT
            - SELECTION_MODE_ALWAYS_ASK
            - SELECTION_MODE_ASK_IF_CONFLICT

        returns int value.
        '''
        category = kwargs.get('category')
        return self.card.getSelectionModeForCategory(category)

    def _is_default_service_for_aid(self, **kwargs):
        '''
        Expects 2 parameters:
            - services: componentName
            - aid: String, e.g: The ISO7816-4 Application ID

        Allows an application to query whether a service is currently the
        default handler for a specified ISO7816-4 Application ID.

        returns boolean value.

        '''
        service = kwargs.get('service')
        aid = kwargs.get('aid')
        return self.card.isDefaultServiceForAid(service, aid)

    def _is_default_service_for_category(self, **kwargs):
        '''
        Expects 2 parameters:
            - services: componentName
            - category: String

        Allows an application to query whether a service is currently the
        default service to handle a card emulation category.

        returns boolean value.

        '''
        service = kwargs.get('service')
        category = kwargs.get('category')
        return self.card.isDefaultServiceForCategory(service, category)

    def _register_aids_for_service(self, **kwargs):
        '''
        Expects 3 parameters:
            - services: componentName
            - category: String
            - aids: List, containing the AIDs to be registered.


        Note that you can only register AIDs for a service that is running
        under the same UID as the caller of this API.

        returns boolean value.

        '''
        service = kwargs.get('service')
        category = kwargs.get('category')
        aids = kwargs.get('aids')
        return self.card.registerAidsForService(service, category, aids)

    def _remove_aids_for_service(self, **kwargs):
        '''
        Expects 2 parameters:
            - services: componentName
            - category: String

        Note that this will only remove AIDs that were dynamically registered
        using the registerAidsForService(ComponentName, String, List) method.

        returns boolean value.

        '''
        service = kwargs.get('service')
        category = kwargs.get('category')
        return self.card.removeAidsForService(service, category)

    def _set_preferred_service(self, **kwargs):
        '''
        Expects 2 parameters:
            - activity: Activity
            - services: componentName

        Allows a foreground application to specify which card emulation service
        should be preferred while a specific Activity is in the foreground.

        preferred to be called in the `on_resume` method.

        returns boolean value.

        '''
        service = kwargs.get('service')
        activity = kwargs.get('activity')
        return self.card.setPreferredService(activity, service)

    def _unset_preferred_service(self, **kwargs):
        '''
        Expects 1 parameters:
            - activity: Activity

        Unsets the preferred service for the specified Activity.

        preferred to be called in the `on_pause` method.

        returns boolean value.

        '''
        activity = kwargs.get('activity')
        return self.card.unsetPreferredService(activity)

    def _support_aid_prefix_registration(self):
        '''
        Expects 0 parameters:

        Some devices may allow an application to register all AIDs
        that starts with a certain prefix.
        e.g. "A000000004*" to register all MasterCard AIDs.

        returns boolean value.
        '''
        return self.card.supportsAidPrefixRegistration()

    # -------------------------------------------
    # Reference API for NfcFCardEmulation class.
    # -------------------------------------------

    def _disable_service(self, **kwargs):
        '''
        Expects 1 parameters:
            - activity: Activity

        Disables the service for the specified Activity.

        preferred to be called in `on_pause` method.

        returns boolean value.
        '''
        try:
            activity = kwargs.get('activity')
            return self.nfcf_card.disableService(activity)
        except:
            raise RuntimeError('Unable to disable service.')

    def _enable_service(self, **kwargs):
        '''
        Expects 2 parameters:
            - activity: Activity
            - services: componentName

        Allows a foreground application to specify which card emulation service
        should be enabled while a specific Activity is in the foreground.

        preferred to be called in `on_resume method`

        returns boolean value.
        '''
        try:
            activity = kwargs.get('activity')
            service = kwargs.get('service')
            return self.nfcf_card.enableService(activity, service)
        except:
            raise RuntimeError('Unable to enable service.')

    def _set_nfcid2_for_service(self, **kwargs):
        '''
        Expects 2 parameters:
            - services: componentName
            - nfcid2: String

        NFCID2 must be in range from "02FE000000000000" to "02FEFFFFFFFFFFFF".

        returns boolean value
        '''
        try:
            service = kwargs.get('service')
            nfcid2 = kwargs.get('nfcid2')
            self.nfcf_card.setNfcid2ForService(service, nfcid2)
        except:
            raise RuntimeError('Unable to set Nfcid2 for service.')

    def _get_nfcid2_for_service(self, **kwargs):
        '''
        Expects 1 parameters:
            - services: componentName

        Retrieves the current NFCID2 for the specified service.

        returns String value.
        '''
        try:
            service = kwargs.get('service')
            return self.nfcf_card.getNfcid2ForService()
        except:
            raise RuntimeError('Unable to get Nfcid2 for Service.')

    def _get_system_code_for_service(self, **kwargs):
        '''
        Expects 1 parameter:
            - service: componentName

        Retrieves the current System Code for the specified service.

        returns string value.
        '''
        try:
            self.nfcf_card.getSystemCodeForService(service)
        except:
            raise RuntimeError('Unable to get system code for service.')

    def _register_system_code_for_service(self, **kwargs):
        '''
        Expects 2 parameters:
            - service: componentName
            - system_code: String

        Registers a System Code for the specified service.
        The System Code must be in range from "4000" to "4FFF"
        (excluding "4*FF").

        returns boolean value.
        '''
        try:
            service = kwargs.get('service')
            system_code = kwargs.get('system_code')
            self.nfcf_card.registerSystemCodeForService(service, system_code)
        except:
            raise RuntimeError('Unable to register system code for service.')

    def _unregister_system_code_for_service(self, **kwargs):
        '''
        Expects 1 parameter:
            - service: componentName

        Removes a registered System Code for the specified service.

        returns boolean value.
        '''
        try:
            service = kwargs.get('service')
            self.nfcf_card.unregisterSystemCodeForService(service)
        except:
            raise RuntimeError('Unable to unregister system code for service.')

    def _on_pause(self):
        '''
        Handles stuff when the application pauses.
        '''
        self._disable()

    def _on_resume(self):
        '''
        Handles stuff when the application resumes.
        '''
        self._enable()


def instance():
    return AndroidNFC()
