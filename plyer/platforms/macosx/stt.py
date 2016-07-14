from plyer.facades import STT
from pyobjus import autoclass, objc_arr, objc_str, protocol, selector
from pyobjus.dylib_manager import load_framework, INCLUDE

load_framework(INCLUDE.AppKit)

NSSpeechRecognizer = autoclass('NSSpeechRecognizer')
NSString = autoclass('NSString')


class SpeechToText(STT):

    def _ns(self, x):
        NSString.alloc().initWithUTF8String_(x)

    def _start_listening(self, **kwargs):
        self.obj = NSSpeechRecognizer.alloc()
        self.obj.init()
        # self.obj_delegate = NSSpeechRecognizerDelegate
        self.obj.commands = ["a", "b", "c"]
        self.obj.setDelegate_(self)
        self.obj.startListening()

        # foo(NSSpeechRecognizerDelegate, "")

    @protocol('NSSpeechRecognizerDelegate')
    def speechRecognizer_didRecognizeCommand_(self, sender, command):
        print command
        try:
            cnt = command.allObjects().count()
            for i in range(cnt):
                print command.allObjects().objectAtIndex_(i).UTF8String()
        except:
            pass

    def _set_commands(self):
        self.obj.commands = ["a", "b", "c"]
        self.obj.setCommands_ = ["a", "b", "c"]

    def _display_commands_title(self):
        return self.obj.delegate
        # return self.obj.displayedCommandsTitle

    def _display_commnds(self):
        return self.obj.commands

    def _stop_listening(self, **kwargs):
        self.obj.stopListening()
        print "Not Listening"


def foo(name, string):
    matching = []
    matching = [s for s in dir(name) if "{}".format(string) in s]
    for m in matching:
        print m


def instance():
    return SpeechToText()
