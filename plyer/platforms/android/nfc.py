from jnius import autoclass, cast
from android.runnable import run_on_ui_thread
from android import activity
from plyer.facades import NFC

NfcAdapter = autoclass('android.nfc.NfcAdapter')
PythonActivity = autoclass('org.renpy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
IntentFilter = autoclass('android.content.IntentFilter')
PendingIntent = autoclass('android.app.PendingIntent')
JavaString = autoclass('java.lang.String')
# Imports for Beam #
Arraylist = autoclass('java.util.ArrayList')
Uri = autoclass('android.net.Uri')
File = autoclass('java.io.File')
# End Beam imports
BUILDVERSION = autoclass('android.os.Build$VERSION').SDK_INT
NdefRecord = autoclass('android.nfc.NdefRecord')
# immutable NDEF Record.
NdefMessage = autoclass('android.nfc.NdefMessage')
# Immutable ndef message.
Tag = autoclass('android.nfc.Tag')
# Represents discovered NDC tag.
IsoDep = autoclass('android.nfc.tech.IsoDep')
# Provides access to IOS_DEP(ISO 14443-4) properties and I/O operations.
MifareClassic = autoclass('android.nfc.tech.MifareClassic')
# Provides access to MIFARE Classic properties and I/O operations,
# If device supports MIFARE.
MifareUltralight = autoclass('android.nfc.tech.MifareUltralight')
# Provides access to MIFARE Ultralight properties and I/O operations,
# If device supports MIFARE.
Ndef = autoclass('android.nfc.tech.Ndef')
# Provides access to NDEF data and operations on NFC tags that have been
# formatted as NDEF.
NdefFormatable = autoclass('android.nfc.tech.NdefFormatable')
# Provides a format operations for the tags that may be NDEF formattable.
NfcManager = autoclass('android.nfc.NfcManager')
# Used to obtain an instance instance of NfcAdapter.
NfcEvent = autoclass('android.nfc.NfcEvent')
# Information associated with NFC events


class PyNdefRecord(NFC.NdefRecord):

    def __init__(self, **kwargs):
        pass
        # self.ndef_type = ndef_type
        # self.payload = payload
        # if self.ndef_type == 'application':
        #     return self._create_application_record(payload)

    def __call__(self, **kwargs):

        payload = kwargs.get("payload")
        ndef_type = kwargs.get("ndef_type")
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
            return

    def _create_application_record(self, **kwargs):
        payload = kwargs.get('payload')
        package_name = payload.get('package_name')
        return NdefRecord.createApplicationRecord(JavaString(package_name))

    def _create_external(self, **kwargs):
        payload = kwargs.get('payload')
        domain = payload.get('domain')
        external_type = payload.get('external_type')
        data = kwargs.get('data')
        if BUILDVERSION > 16:
            return NdefRecord.createExternal(JavaString(domain),
                                             JavaString(external_type),
                                             data)
        record = NdefRecord(NdefRecord.TNF_EXTERNAL_TYPE,
                            "{} + ':' + {}".format(JavaString(domain),
                                                   JavaString(external_type)),
                            '',
                            payload)
        return record

    def _create_mime(self, **kwargs):
        payload = kwargs.get('payload')
        mime_type = payload.get('mime_type')
        mime_data = payload.get('mime_data')
        if BUILDVERSION > 16:
            return NdefRecord.createMime(JavaString(mime_type),
                                         mime_data)
        record = NdefRecord(NdefRecord.TNF_MIME_MEDIA,
                            JavaString(mime_type),
                            '',
                            payload)
        return record

    def _create_text_record(self, **kwargs):
        payload = kwargs.get('payload')
        language_code = payload.get('language_code')
        text = kwargs.get('text')
        if BUILDVERSION > 21:
            return NdefRecord.createTextRecord(JavaString(language_code),
                                               JavaString(text))
        record = NdefRecord(NdefRecord.TNF_WELL_KNOWN,
                            language_code,
                            '',
                            text)
        return record

    def _create_uri(self, **kwargs):
        payload = kwargs.get('payload')
        uri = payload.get('uri')
        if BUILDVERSION > 14:
            return NdefRecord.createUri(JavaString(uri))

        record = NdefRecord(NdefRecord.TNF_WELL_KNOWN,
                            NdefRecord.RTD_URI,
                            '',
                            uri)
        return record

    def _create_RTD_ALTERNATIVE_CARRIER(self, **kwargs):
        payload = kwargs.get('payload')
        data = payload.get('alterative_carrier')
        record = NdefRecord(NdefRecord.TNF_WELL_KNOWN,
                            NdefRecord.RTD_ALTERNATIVE_CARRIER,
                            '',
                            data)
        return record

    def _create_RTD_HANDOVER_CARRIER(self, **kwargs):
        payload = kwargs.get('payload')
        data = payload.get('handover_carrier')
        record = NdefRecord(NdefRecord.TNF_WELL_KNOWN,
                            NdefRecord.RTD_HANDOVER_CARRIER,
                            '',
                            data)
        return record

    def _create_RTD_HANDOVER_REQUEST(self, **kwargs):
        payload = kwargs.get('payload')
        data = payload.get('handover_request')
        record = NdefRecord(NdefRecord.TNF_WELL_KNOWN,
                            NdefRecord.RTD_HANDOVER_REQUEST,
                            '',
                            data)
        return record

    def _create_RTD_HANDOVER_SELECT(self, **kwargs):
        payload = kwargs.get('payload')
        data = payload.get('handover_select')
        record = NdefRecord(NdefRecord.TNF_WELL_KNOWN,
                            NdefRecord.RTD_HANDOVER_SELECT,
                            '',
                            data)
        return record

    def _create_RTD_SMART_POSTER(self, **kwargs):
        payload = kwargs.get('payload')
        data = payload.get('smart_poster')
        record = NdefRecord(NdefRecord.TNF_WELL_KNOWN,
                            NdefRecord.RTD_SMART_POSTER,
                            '',
                            data)
        return record

    def _create_RTD_TEXT(self, **kwargs):
        payload = kwargs.get('payload')
        data = payload.get('text')
        record = NdefRecord(NdefRecord.TNF_WELL_KNOWN,
                            NdefRecord.RTD_TEXT,
                            '',
                            data)
        return record


class AndroidNFC(NFC):

    tag_message = ''

    '''
    some methods adapted from
    `https://gist.github.com/tito/9e2308a4c942ddb2342b`
    and
    `https://gist.github.com/akshayaurora/b76dbcc69c9850bb3e318af4722a0b4f`

    some methods inspired from
    `https://developer.android.com/reference/android/nfc/package-summary.html`
    '''
    def nfc_init(self):
        '''
        Initializing NFC adapter and listing the techs available.
        '''

        self.j_context = context = PythonActivity.mActivity
        self.nfc_adapter = NfcAdapter.getDefaultAdapter(context)
        if not nfc_adapter:
            return
        self.nfc_pending_intent = PendingIntent.getActivity(context, 0,
                                  Intent(context, context.getClass()).addFlags(
                                         Intent.FLAG_ACTIVITY_SINGLE_TOP), 0)

        self.ndef_detected = IntentFilter(NfcAdapter.ACTION_NDEF_DISCOVERED)
        self.tech_detected = IntentFilter(NfcAdapter.ACTION_TECH_DISCOVERED)
        self.tag_detected = IntentFilter(NfcAdapter.ACTION_TAG_DISCOVERED)

        self.ndef_detected.addDataType('*/*')
        self.tech_detected.addDataType('*/*')
        self.tag_detected.addDataType('*/*')

        self.ndef_tech_list = [
            ['android.nfc.tech.IsoDep'],
            ['android.nfc.tech.NfcA'],
            ['android.nfc.tech.NfcB'],
            ['android.nfc.tech.NfcF'],
            ['android.nfc.tech.NfcV'],
            ['android.nfc.tech.Ndef'],
            ['android.nfc.tech.NdefFormattable'],
            ['android.nfc.tech.MifareClassic']
            ['android.nfc.tech.MifareUltralight'],
            ]

        self.ndef_exchange_filters = [
            self.ndef_detected,
            self.tech_detected,
            self.tag_detected
            ]

        self._enable()
        self._on_new_intent(PythonActivity.getIntent())
        return True

    def _disable(self):
        activity.unbind(on_new_intent=self._on_new_intent)
        self._disable_foreground_dispatch()

    def _enable(self):
        activity.bind(on_new_intent=self._on_new_intent)
        self._enable_foreground_dispatch()

    # Returns android NdefRecord object.
    def _write_record(self, ndef_type, payload):
        '''
        For writing android NdefRecords.
        '''
        record = PyNdefRecord()
        return record(ndef_type, payload)

    def _read_record(self):
        '''
        Reading android NdefRecords.
        '''
        return

    '''
    method adapted from `https://gist.github.com/tito/9e2308a4c942ddb2342b`
    '''
    @run_on_ui_thread
    def _nfc_enable_ndef_exchange(self, **kwargs):
        ndef_record = NdefRecord(
                NdefRecord.TNF_MIME_MEDIA,
                'text/plain', '', 'hello world')
        ndef_message = NdefMessage([ndef_record])

        self.nfc_adapter.enableForegroundNdefPush(self.j_context, ndef_message)

        self.nfc_adapter.enableForegroundDispatch(self.j_context,
                self.nfc_pending_intent, self.ndef_exchange_filters, [])

    '''
    method adapted from `https://gist.github.com/tito/9e2308a4c942ddb2342b`
    '''
    @run_on_ui_thread
    def _nfc_disable_ndef_exchange(self):
        self.nfc_adapter.disableForegroundNdefPush(self.j_context)
        self.nfc_adapter.disableForegroundDispatch(self.j_context)

    @run_on_ui_thread
    def _disable_foreground_dispatch(self):
        self.nfc_adapter.disableForegroundDispatch(self.j_context)

    @run_on_ui_thread
    def _enable_foreground_dispatch(self):
        self.nfc_adapter.enableForegroundDispatch(self.j_context,
                                                  self.nfc_pending_intent,
                                                  self.ndef_exchange_filters,
                                                  self.ndef_tech_list)

    def _nfc_enable_exchange(self, **kwargs):
        data = kwargs.get('data')
        self._nfc_enable_ndef_exchange(data)

    def _nfc_disable_exchange(self):
        self._nfc_disable_ndef_exchange()

    def _on_new_intent(self, intent):
        if intent.getAction() == NfcAdapter.ACTION_NDEF_DISCOVERED:

            extra_msgs = intent.getParcelableArrayExtra(
                                NfcAdapter.EXTRA_NDEF_MESSAGES)
            # An array of NDEF messages parsed from the tag.
            if not extra_msgs:
                return

            for message in extra_msgs:
                message = cast(NdefMessage, message)
                payload = message.getRecords()[0].getPayload()

            extra_tag = intent.getParcelableExtra(NfcAdapter.EXTRA_TAG)
            # Tag object representing the scanned tag.
            extra_ID = intent.getParcelableExtra(NfcAdapter.EXTRA_ID)
            # Low Level ID of the tag
            return {'payload': {}.format(''.join(map(chr, payload))),
                    'tag': extra_tag,
                    'id': extra_ID}

        elif intent.getAction() == NfcAdapter.ACTION_TECH_DISCOVERED:
            return

        elif intent.getAction() == NfcAdapter.ACTION_TAG_DISCOVERED:
            # If tag is discovered.
            self._get_tag_info(intent)

    # P2P

    def _nfc_beam(self, **kwargs):
        files = kwargs.get('files')
        filesUris = Arraylist()
        for i in range(len(files)):
            share_file = File(files[i])
            uri = Uri.fromFile(share_file)
            filesUris.add(uri)

        self.nfc_adapter.setBeamPushUris(filesUris, self.j_context)

    # TAG reading and writing.

    def _get_tag_info(self, intent):
        '''
        Reading the tags of the type listed in the ndef_tech_list.
        '''

        tag = intent.getParcableExtra(NfcAdapter.EXTRA_TAG)
        taglist = tag.getTechList()

        for i in range(len(taglist)):
            if taglist[i] == MifareClassic.class.getName():
                mctag = MifareClassic.get(tag)
                mctag_type = mctag.getType()

                if (mctag_type == MifareClassic.TYPE_CLASSIC):
                    mfc = MifareClassic.get(tag)
                    pass

                elif (mctag_type == MifareClassic.TYPE_PLUS):
                    pass

                elif (mctag_type == MifareClassic.TYPE_PRO):
                    pass

            elif taglist[i] == MifareUltralight.class.getName():
                mutag_type = mutag.getType()

                if (mutag_type == MifareUltralight.TYPE_ULTRALIGHT):
                    self._read_ultra_tag(tag)

                elif (mutag_type == MifareUltralight.TYPE_ULTRALIGHT_C):
                    pass

            elif taglist[i] == IsoDep.class.getName():
                self._read_isodep_rag(tag)

            elif taglist[i] == Ndef.class.getName():
                self._read_ndef_tag(tag)

            elif taglist[i] == NdefFormatable.class.getName():
                self._read_ndef_formattable_tag(tag)

    def _read_classic_tag(self, Tag):
        return

    def _read_ultra_tag(self, Tag):
        mifare = MifareUltralight.get(tag)

        try:
            mifare.connect()
            payload = mifare.readPages(4)
            self.tag_message = str(payload, Charset.forName("US-ASCII"))
            return str(payload, Charset.forName("US-ASCII"))

        except:
            return

        finally:
            mifare.close()

    def _read_iso_dep_tag(self):
        return

    def _read_ndef_tag(self, Tag):
        return

    def _read_iso_dep_tag(self, Tag):
        return

    def _read_ndef_formattable_tag(self, Tag):
        return

    def write_tag(self, Tag, tagText):
        return

    def _write_classic_tag(self, Tag, tagText):
        return

    def _write_ultra_tag(self, Tag, tagText):
        ''' MifareUltralight tags contains 16 pages and each page contains
        4 bytes. It's first four page contains manufacturer info, OTP and
        locking bytes.
        Page data must be equal 4 bytes and page number must be less than 16.
        '''

        ultralight = MifareUltralight.get(Tag)
        try:
            ultralight.connect()
            ultralight.writePage(4, tagText.encode())

        except:
            return

        finally:
            ultralight.close()

    def _write_ndef_tag(self, Tag, tagText):

        ndef_record = NdefRecord(
                NdefRecord.TNF_WELL_KNOWN,
                NdefRecord.RTD_TEXT,
                tagText)
        ndef_message = NdefMessage([ndef_record])
        ndef = Ndef.get(Tag)
        ndef.connect()
        ndef.writeNdefMessage(tagText)
        ndef.close()

    def _write_isodep_tag(self, Tag, tagText):
        return

    def _write_ndef_formattable_tag(self, Tag, tagText):
        return

    def _on_pause(self):
        self._disable()

    def _on_resume(self):
        self._enable()


def instance():
    return AndroidNFC()
