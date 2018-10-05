from plyer.facades import Audio
from pyobjus.dylib_manager import load_framework, INCLUDE
from pyobjus import autoclass, objc_str

load_framework(INCLUDE.Foundation)
load_framework(INCLUDE.AVFoundation)

AVAudioRecorder = autoclass("AVAudioRecorder")
AVAudioFormat = autoclass("AVAudioFormat")
NSString = autoclass('NSString')
NSURL = autoclass('NSURL')

class OSXAudio(Audio):
    def __init__(self, file_path=None):
        default_path = '/Users/maroskovac/Dev/audio.wav'
        super(OSXAudio, self).__init__(file_path or default_path)

        self._recorder = None
        self._player = None

    def _start(self):
        # filePathNSString = NSString.alloc().initWithUTF8String_(self._file_path)

        fileNSURL = NSURL.alloc().initWithString_(
            objc_str(self._file_path)
        )

        af = AVAudioFormat.alloc()
        af = af.initWithCommonFormat_sampleRate_channels_interleaved_(
            1, 44100.0, 2, True
        )

        self._recorder = AVAudioRecorder.alloc().initWithURL_format_error_(fileNSURL, af, None)
        
        if self._recorder:
            print("Recording...")
            self._recorder.record()

    def _stop(self):
        if self._recorder:
            self._recorder.stop()
            print("Stopped recording.")
            self._recorder = None

def instance():
    return OSXAudio()
