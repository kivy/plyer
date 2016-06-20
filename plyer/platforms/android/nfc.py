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
NfcA = autoclass('android.nfc.tech.NfcA')
NfcB = autoclass('android.nfc.tect.NfcB')
NfcF = autoclass('android.nfc.tech.NfcF')
NfcV = autoclass('android.nfc.tech.NfcV')
NfcBarcode = autoclass('android.nfc.tech.NfcBarcode')
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
        self.nfc_pending_intent = PendingIntent.getActivity(context,
                                                            0,
                                  Intent(context,
                                         context.getClass()).addFlags(
                                         Intent.FLAG_ACTIVITY_SINGLE_TOP),
                                                            0)

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
            ['android.nfc.tech.NfcBarcode'],
            ['android.nfc.tech.NdefFormattable'],
            ['android.nfc.tech.MifareClassic'],
            ['android.nfc.tech.MifareUltralight']]

        self.ndef_exchange_filters = [
            self.ndef_detected,
            self.tech_detected,
            self.tag_detected]

        self.tag_mode = 'read'
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

    def _read_record(self, record):
        '''
        Reading android NdefRecords.
        '''
        return

    def _read_ndef_message(self, messages):
        '''
        Reading android NdefMessage.
        '''
        if not messages:
            return

        for message in messages:
            message = cast(NdefMessage, message)
            payload = message.getRecords()[0].getPayload()
        return payload

    def _create_ndef_message(self, *records):
        '''
        NdefMessage that will be written on tag.
        '''
        return NdefMessage([record for record in records if record])

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
                                                  self.nfc_pending_intent,
                                                  self.ndef_exchange_filters,
                                                  [])

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
            payload = self._read_ndef_message(extra_msgs)

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
            return self._get_tag_info(intent)

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

    def _set_tag_mode(self, mode):
        '''
        Set the Tag mode from two choices.
        Read and right.
        '''
        self.tag_mode = mode

    @property
    def _get_tag_mode(self):
        '''
        Get the tag mode.
        '''
        return self.tag_mode

    def _get_tag_info(self, intent):
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
            return details

    def _read_ultra_tag(self, Tag):
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
            return details

    def _read_iso_dep_tag(self, tag):
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
            return details

    def _read_ndef_tag(self, tag):
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
                    'payload': ''.join(map(chr, record.getPayload()))
                    })

            details['recTypes'] = recTypes
            tech_tag.close()
        except:
            raise Exception('Either Tag is lost or I/O failure.')
        finally:
            return details

    def _read_nfcA_tag(self, tag):
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
            return details

    def _read_nfcB_tag(self, tag):
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
            return details

    def _read_nfcF_tag(self, tag):
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
            return details

    def _read_nfcV_tag(self, tag):
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
            return details

    def _read_nfc_barcode_tag(self, tag):
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
            return details

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
        '''
        tech_tag = cast('android.nfc.tech.IsoDep', IsoDep.get(tag))
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
        '''
        tech_tag = cast('android.nfc.tech.IsoDep', IsoDep.get(tag))
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

    def _on_pause(self):
        self._disable()

    def _on_resume(self):
        self._enable()


def instance():
    return AndroidNFC()
