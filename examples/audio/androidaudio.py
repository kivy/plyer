from time import sleep

from jnius import autoclass
from jnius import cast
from jnius import java_method
from jnius import PythonJavaClass

# from plyer.facades import Microphone
# from plyer.facades import MICROPHONE_STATUS
from audio import Microphone, MICROPHONE_STATUS
from plyer.platforms.android import activity
from plyer.platforms.android import SDK_INT

# Java Classes
FileInputStream = autoclass('java.io.FileInputStream')
SequenceInputStream = autoclass('java.io.SequenceInputStream')

# Android Classes

# Recorder Classes
MediaRecorder = autoclass('android.media.MediaRecorder')
AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
OutputFormat = autoclass('android.media.MediaRecorder$OutputFormat')
AudioEncoder = autoclass('android.media.MediaRecorder$AudioEncoder')

# Player Classes
MediaPlayer = autoclass('android.media.MediaPlayer')

OUTPUT_FORMAT = {
    'default': OutputFormat.DEFAULT,  # 0x0000

    # 3GPP media file format
    'three_gpp': OutputFormat.THREE_GPP,  # 0x0001

    # MPEG4 media file format
    'mpeg_4': OutputFormat.MPEG_4,  # 0x0002

    # AMR NB file format, deprecated in api>=16
    'raw_amr': OutputFormat.RAW_AMR,  # 0x0003

    # AMR NB file format, SDK_INT >= 10
    'amr_nb': OutputFormat.AMR_NB,  # 0x0003

    # AMR WB file format, SDK_INT >= 10
    'amr_wb': OutputFormat.AMR_WB,  # 0x0004

    # AAC ADTS file format, SDK_INT >= 16
    'acc_adts': OutputFormat.AAC_ADTS,  # 0x0006

    # VP8/VORBIS data in a WEBM container, SDK_INT >= 21
    'webm': OutputFormat.WEBM,  # 0x0009
}


AUDIO_ENCODER = {
    'default': AudioEncoder.DEFAULT,  # 0x0000

    # AMR (Narrowband) audio codec
    'amr_nb': AudioEncoder.AMR_NB,  # 0x0001

    # AMR (Wideband) audio codec
    'amr_wb': AudioEncoder.AMR_WB,  # 0x0002

    # AAC Low Complexity (AAC-LC) audio codec
    'acc': AudioEncoder.AAC,  # 0x0003

    # High Efficiency AAC (HE-AAC) audio codec
    'he_aac': AudioEncoder.HE_AAC,  # 0x0004

    # Enhanced Low Delay AAC (AAC-ELD) audio codec
    'acc_eld': AudioEncoder.AAC_ELD,  # 0x0005

    # Ogg Vorbis audio codec
    'vorbis': AudioEncoder.VORBIS,  # 0x0006
}

AUDIO_SOURCE = {
    # Default audio source
    'default': AudioSource.DEFAULT,  # 0x0000,

    # Microphone audio source
    'microphone': AudioSource.MIC,  # 0x0001

    # Voice call uplink (Tx) audio source
    'voice_uplink': AudioSource.VOICE_UPLINK,  # 0x0002

    # Voice call downlink (Rx) audio source
    'voice_downlink': AudioSource.VOICE_DOWNLINK,  # 0x0003

    # # Voice call uplink + downlink audio source
    'voice_call': AudioSource.VOICE_CALL,  # 0x0004

    # Microphone audio source with same orientation as camera if available,
    # the main device microphone otherwise
    'camcorder': AudioSource.CAMCORDER,  # 0x0005

    # Microphone audio source tuned for voice recognition if available,
    # behaves like DEFAULT otherwise.
    'voice_recognition': AudioSource.VOICE_RECOGNITION,  # 0x0006

}


class AndroidMicrophone(Microphone):
    """Microphone for android.
    .. note::
         Android recorder doesnt handles `pause` and `resume` by default.
         In order to have these features, recorder saves recording in
         temporary file.
         On pause or on stop, recorder merges content from temporary file
         with file from given location.
    """

    # needed for pause and resume
    _temp_path = '/sdcard/temp.3gp'

    # keeps current options like source, format or encoders
    _options = {}

    def __init__(self, file_path=None):
        default_path = '/sdcard/testrecorder.3gp'
        super(AndroidMicrophone, self).__init__(file_path or default_path)

    def _start(self):
        self._recorder = MediaRecorder()
        self._recorder.setAudioSource(AUDIO_SOURCE['microphone'])
        self._recorder.setOutputFormat(OUTPUT_FORMAT['three_gpp'])
        self._recorder.setAudioEncoder(AUDIO_ENCODER['default'])
        self._recorder.setOutputFile(self._temp_path)

        self._recorder.prepare()
        self._recorder.start()
        self.status = MICROPHONE_STATUS['recording']

    def _stop(self):
        self._recorder.stop()
        self._recorder.release()
        self._recorder = None
        self._merge()
        self.status = MICROPHONE_STATUS['stopped']

    def _pause(self):
        if self.status == MICROPHONE_STATUS['pause']:
            # do un-pause if there is pause already
            self._start()
        else:
            self._stop()
            self.status = MICROPHONE_STATUS['pause']

    def _resume(self):
        self._start()

    def _play(self):
        media_player = MediaPlayer(activity)
        media_player.setDataSource(self.file_path)
        media_player.prepare()
        media_player.start()
        self.status = MICROPHONE_STATUS['play']

    def _info(self):
        return self._options

    def _merge(self):
        """Merge temporary recording with original recording."""
        temp = FileInputStream(self._temp_path)
        orig = FileInputStream(self._file_path)

        stream = SequenceInputStream(temp, orig)
        while True:
            data = stream.read()
            if data == -1:
                break
            orig.write(data)
