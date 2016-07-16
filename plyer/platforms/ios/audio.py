from pyobjus import autoclass, objc_arr, objc_str, protocol, selector
from pyobjus.dylib_manager import load_framework, INCLUDE
from plyer.facades import Audio
load_framework(INCLUDE.AVFoundation)
AVAudioRecorder = autoclass('AVAudioRecorder')
NSURL = autoclass('NSURL')
NSMutableDictionary = autoclass('NSMutableDictionary')


class IosAudio(Audio):

    def __init__(self, file_path=None):
        default_path = './testrecorder.3gp'
        super(IosAudio, self).__init__(file_path or default_path)

    def _start(self):
        url = NSURL.alloc().initWithString_(objc_str(self.file_path))
        # settings = NSMutableDictionary.alloc().init()
        default_settings = {
            AVFormatIDKey = 1768775988,
            AVLinearPCMBitDepthKey = 16,
            AVLinearPCMIsBigEndianKey = 0,
            AVLinearPCMIsFloatKey = 0,
            AVNumberOfChannelsKey = 2,
            AVSampleRateKey = 44100}

        self.recorder = AVAudioRecorder.alloc()
        self.recorder.initWithURL_settings_error(url,
                                                 default_settings,
                                                 None)
        # self.recorder.delegate = self
        self.recorder.prepareToRecord()
        self.recorder.record()

    @protocol('AVAudioRecorderDelegate')
    def audioRecorderDidFinishRecording_successfully(self, recorder, flag):
        '''
        Called by the system when a recording is stopped or has finished due
        to reaching its time limit.
        '''
        return flag

    @protocol('AVAudioRecorderDelegate')
    def audioRecorderEncodeErrorDidOccur_error(self, recorder, error=None):
        '''
        Called when an audio recorder encounters an encoding error during
        recording.
        '''
        return error

    def _stop(self):
        self.recorder.stop()

    def _pause(self):
        self.recorder.pause()

    def _play(self):
        pass


def instance():
    return IosAudio()
