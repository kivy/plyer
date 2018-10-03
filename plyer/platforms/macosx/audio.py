from plyer.facades import Audio
from pyobjus.dylib_manager import load_framework, INCLUDE
from pyobjus import autoclass

load_framework(INCLUDE.Foundation)
load_framework(INCLUDE.AVFoundation)

AVAudioRecorder = autoclass("AVAudioRecorder")
AVAudioFormat = autoclass("AVAudioFormat")
NSString = autoclass('NSString')
NSURL = autoclass('NSURL')

class OSXAudio(Audio):
    def __init__(self, file_path=None):
        default_path = '~/Desktop/testrecording.wav'
        super(OSXAudio, self).__init__(file_path or default_path)

        self._recorder = None
        self._player = None

    def _start(self):
        filePathNSString = NSString.alloc().initWithUTF8String_(self._file_path)
        fileNSURL = NSURL.alloc().initFileURLWithPath_(filePathNSString)
        af = AVAudioFormat.alloc()
        af = af.initWithCommonFormat_sampleRate_channels_interleaved_(
            1, 44100, 1, True
        )

        self._recorder = AVAudioRecorder.alloc().initWithURL_format_error_(fileNSURL, fileAudioFormat, None)
    
def instance():
    return OSXAudio();