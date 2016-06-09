from jnius import autoclass, cast
from android.runnable import run_on_ui_thread
from android import activity
from plyer.facades import NFC

NfcAdapter = autoclass('android.nfc.NfcAdapter')
PythonActivity = autoclass('org.renpy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
IntentFilter = autoclass('android.content.IntentFilter')
PendingIntent = autoclass('android.app.PendingIntent')
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


class AndroidNFC(NFC):

    tag_message = ''

    def nfc_init(self):

        self.j_context = context = PythonActivity.mActivity
        self.nfc_adapter = NfcAdapter.getDefaultAdapter(context)
        self.nfc_pending_intent = PendingIntent.getActivity(context, 0,
                                Intent(context, context.getClass()).addFlags(
                                       Intent.FLAG_ACTIVITY_SINGLE_TOP), 0)

        print 'p2p filter'
        self.ndef_detected = IntentFilter(NfcAdapter.ACTION_NDEF_DISCOVERED)
        self.ndef_detected.addDataType('text/plain')
        self.ndef_exchange_filters = [self.ndef_detected]

    def _on_new_intent(self, intent):
        # print 'on_new_intent()', intent.getAction()
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
            return {'payload': '{}'.format(''.join(map(chr, payload)),
                    'tag': extra_tag,
                    'id': extra_ID}

        elif intent.getAction() == NfcAdapter.ACTION_TECH_DISCOVERED:
            pass

        elif intent.getAction() == NfcAdapter.ACTION_TAG_DISCOVERED:
            # If tag is discovered.
            self._get_tag_info(intent)

    def _get_tag_info(self, intent):

        tag=intent.getParcableExtra(NfcAdapter.EXTRA_TAG)
        taglist=tag.getTechList()

        for i in range(len(taglist)):
            if taglist[i] == MifareClassic.class.getName():
                mctag=MifareClassic.get(tag)
                mctag_type=mctag.getType()

                if (mctag_type == MifareClassic.TYPE_CLASSIC):
                    mfc=MifareClassic.get(tag)
                    pass

                elif (mctag_type == MifareClassic.TYPE_PLUS):
                    pass

                elif (mctag_type == MifareClassic.TYPE_PRO):
                    pass

            elif taglist[i] == MifareUltralight.class.getName():
                mutag_type=mutag.getType()

                if (mutag_type == MifareUltralight.TYPE_ULTRALIGHT):
                    self._read_ultra_tag(tag)

                elif (mutag_type == MifareUltralight.TYPE_ULTRALIGHT_C):
                    pass

            elif taglist[i] == IsoDep.class.getName():
                pass

            elif taglist[i] == Ndef.class.getName():
                self._read_ndef_tag(tag)

            elif taglist[i] == NdefFormatable.class.getName():
                pass


    def _write_ultra_tag(self, Tag, tagText):
        ''' MifareUltralight tags contains 16 pages and each page contains
        4 bytes. It's first four page contains manufacturer info, OTP and
        locking bytes.
        Page data must be equal 4 bytes and page number must be less than 16.
        '''

        ultralight=MifareUltralight.get(Tag)
        try:
            ultralight.connect()
            ultralight.writePage(4, tagText.encode())

        except:
            return

        finally:
            ultralight.close()

    def _write_ndef_tag(self, Tag, tagText):

        ndef_record=NdefRecord(
                NdefRecord.TNF_WELL_KNOWN,
                NdefRecord.RTD_TEXT,
                tagText)
        ndef_message=NdefMessage([ndef_record])
        ndef=Ndef.get(Tag)
        ndef.connect()
        ndef.writeNdefMessage(tagText)
        ndef.close()

    def _read_ultra_tag(self, Tag):
        mifare=MifareUltralight.get(tag)

        try:
            mifare.connect()
            payload=mifare.readPages(4)
            self.tag_message=str(payload, Charset.forName("US-ASCII"))
            return str(payload, Charset.forName("US-ASCII"))

        except:
            return

        finally:
            mifare.close()


    def _read_ndef_tag(self, Tag):
        pass

    def _disable(self):
        activity.unbind(on_new_intent=self._on_new_intent)

    def _enable(self):
        activity.bind(on_new_intent=self._on_new_intent)

    @run_on_ui_thread
    def _nfc_enable_ndef_exchange(self, **kwargs):
        print 'create record'
        ndef_record=NdefRecord(
                NdefRecord.TNF_MIME_MEDIA,
                'text/plain', '', 'hello world')
        print 'create message'
        ndef_message=NdefMessage([ndef_record])

        print 'enable ndef push'
        self.nfc_adapter.enableForegroundNdefPush(self.j_context, ndef_message)

        print 'enable dispatch', self.j_context, self.nfc_pending_intent
        self.nfc_adapter.enableForegroundDispatch(self.j_context,
                self.nfc_pending_intent, self.ndef_exchange_filters, [])

    @run_on_ui_thread
    def _nfc_disable_ndef_exchange(self):
        self.nfc_adapter.disableForegroundNdefPush(self.j_context)
        self.nfc_adapter.disableForegroundDispatch(self.j_context)

    def _on_pause(self):
        self._disable()

    def _on_resume(self):
        self._enable()


def instance():
    return AndroidNFC()
