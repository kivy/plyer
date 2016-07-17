from pyobjus.dylib_manager import load_framework, INCLUDE
from plyer.facades import Audio
from pyobjus import *
from pyobjus.objc_py_types import enum
load_framework(INCLUDE.AVFoundation)
load_framework(INCLUDE.CoreAudio)
AVAudioRecorder = autoclass('AVAudioRecorder')
NSURL = autoclass('NSURL')
NSMutableDictionary = autoclass('NSMutableDictionary')
NSString = autoclass('NSString')


class OSXAudio(Audio):

    def __init__(self, file_path=None):
        default_path = '/Users/kuldeepsingh/Documents/plyer_audio/'
        super(OSXAudio, self).__init__(file_path or default_path)

    def _start(self):
        url = NSURL.alloc().initWithString_(objc_str(self.file_path))
        # settings = NSMutableDictionary.alloc().init()

        FormatId = enum('FormatId',
                        kAudioFormatLinearPCM='lpcm',
                        kAudioFormatAC3='ac-3',
                        kAudioFormat60958AC3='cac3',
                        kAudioFormatAppleIMA4='ima4',
                        kAudioFormatMPEG4AAC='aac ',
                        kAudioFormatMPEG4CELP='celp',
                        kAudioFormatMPEG4HVXC='hvxc',
                        kAudioFormatMPEG4TwinVQ='twvq',
                        kAudioFormatMACE3='MAC3',
                        kAudioFormatMACE6='MAC6',
                        kAudioFormatULaw='ulaw',
                        kAudioFormatALaw='alaw',
                        kAudioFormatQDesign='QDMC',
                        kAudioFormatQDesign2='QDM2',
                        kAudioFormatQUALCOMM='Qclp',
                        kAudioFormatMPEGLayer1='.mp1',
                        kAudioFormatMPEGLayer2='.mp2',
                        kAudioFormatMPEGLayer3='.mp3',
                        kAudioFormatTimeCode='time',
                        kAudioFormatMIDIStream='midi',
                        kAudioFormatParameterValueStream='apvs',
                        kAudioFormatAppleLossless='alac',
                        kAudioFormatMPEG4AAC_HE='aach',
                        kAudioFormatMPEG4AAC_LD='aacl',
                        kAudioFormatMPEG4AAC_ELD='aace',
                        kAudioFormatMPEG4AAC_ELD_SBR='aacf',
                        kAudioFormatMPEG4AAC_HE_V2='aacp',
                        kAudioFormatMPEG4AAC_Spatial='aacs',
                        kAudioFormatAMR='samr',
                        kAudioFormatAudible='AUDB',
                        kAudioFormatiLBC='ilbc',
                        kAudioFormatDVIIntelIMA=0x6D730011,
                        kAudioFormatMicrosoftGSM=0x6D730031,
                        kAudioFormatAES3='aes3')

        d_s = objc_dict({
            'AVFormatIDKey': FormatId.kAudioFormatLinearPCM,
            'AVNumberOfChannelsKey': objc_i(2),
            'AVSampleRateKey': objc_f(44100.0),
            'AVLinearPCMBitDepthKey': objc_i(32),
            'AVLinearPCMIsBigEndianKey': objc_b(False),
            'AVLinearPCMIsFloatKey': objc_b(False)
        })

        self.recorder = AVAudioRecorder.alloc()
        if not self.recorder.initWithURL_settings_error_(url,
                                                         d_s,
                                                         None):
            # print p.localizedDescription
            print foo(self.recorder, "")
            pass
        # self.recorder.delegate = self
        # print self.recorder.prepareToRecord()
        print self.recorder.record()

    @protocol('AVAudioRecorderDelegate')
    def audioRecorderDidFinishRecording_successfully(self, recorder, flag):
        '''
        Called by the system when a recording is stopped or has finished due
        to reaching its time limit.
        '''
        print "Audio recording finished, result: " + str(flag)
        # return flag

    @protocol('AVAudioRecorderDelegate')
    def audioRecorderEncodeErrorDidOccur_error(self, recorder, error=None):
        '''
        Called when an audio recorder encounters an encoding error during
        recording.
        '''
        print "Error occured while recording, error: " + str(error)
        # return error

    def _stop(self):
        self.recorder.stop()

    def _pause(self):
        self.recorder.pause()

    def _play(self):
        pass


def instance():
    return OSXAudio()
