"""
iOS Voip
"""

from pyobjus import autoclass
from plyer.facades import Voip
from kivy.logger import Logger
from pyobjus.dylib_manager import load_framework
from plyer.platforms.ios.frameworks.utils import load_plyer_framework
import threading

load_framework("/System/Library/Frameworks/AVFoundation.framework")
load_framework("/System/Library/Frameworks/Foundation.framework")
load_plyer_framework("Voip.framework")

AVAudioEngine = autoclass("AVAudioEngine")
AVAudioPlayerNode = autoclass("AVAudioPlayerNode")
AVAudioFormat = autoclass("AVAudioFormat")
VoipMachine = autoclass("Voip")
AVAudioSession = autoclass("AVAudioSession")
NSError = autoclass("NSError")


class iOSVoip(Voip):
    input_node = None
    hasPermission = False
    connected = False
    active_call = False
    format = 3
    sample_rate = 16000.0
    channels = 1
    interleaved = False
    buffersize = 640
    error = None
    debug = False

    def __init__(self):
        self.input_node = None
        self.audio_engine = AVAudioEngine.alloc().init()
        self.player_node = AVAudioPlayerNode.alloc().init()
        self.processor = VoipMachine.alloc().init()
        self.processor.audioPlayerNode = self.player_node
        self.processor.inputAudioFormat = (
            AVAudioFormat.alloc()
            .initWithCommonFormat_sampleRate_channels_interleaved_(
                1, 48000.0, 1, False
            )
        )
        self.processor.outputAudioFormat = (
            AVAudioFormat.alloc()
            .initWithCommonFormat_sampleRate_channels_interleaved_(
                self.format, self.sample_rate, self.channels, False
            )
        )
        self.error = NSError.alloc().initWithDomain_code_userInfo_(
            "org.kivy.voip", -1, None
        )

    def verify_permission(self):
        self.hasPermission = False
        self.session = AVAudioSession.sharedInstance()
        record_permission_int = self.session.recordPermission

        if record_permission_int == 1735552628:
            self.hasPermission = True
            if self.debug:
                Logger.info("VOIP: Microphone permission granted")
            return
        if record_permission_int == 1970168948:
            self.hasPermission = self.processor.requestMicrophonePermission()
            self.session = AVAudioSession.sharedInstance()
            record_permission_int = self.session.recordPermission
            if record_permission_int == 1735552628:
                self.hasPermission = True
                if self.debug:
                    Logger.info("VOIP: Microphone permission granted")
                return
        if record_permission_int == 1684369017:
            record_permission = "Denied"
        elif record_permission_int == 1970168948:
            record_permission = "Undetermined"
        else:
            record_permission = "Unknown"

        if self.debug:
            Logger.error(
                f"VOIP: Error: {record_permission} permission. "
                "Ensure NSMicrophoneUsageDescription permission is in "
                "Info.plist and mic access is granted in app settings."
            )

    def configure_audio_session(self):
        session = AVAudioSession.sharedInstance()
        try:
            session.setCategory_mode_options_error_(
                "AVAudioSessionCategoryPlayAndRecord",
                "AVAudioSessionModeVoiceChat",
                0,
                self.error,
            )
            session.setActive_error_(True, self.error)
            if self.debug:
                Logger.info("VOIP: Audio session configured successfully.")
        except Exception as e:
            if self.debug:
                Logger.error(f"VOIP: Failed to configure audio session: {e}")

    def _start_call(self, **kwargs):
        dst_address = kwargs.get("dst_address")
        dst_port = kwargs.get("dst_port")
        client_id = kwargs.get("client_id", "")
        timeout = kwargs.get("timeout", 5)
        ssl = kwargs.get("ssl", False)
        tls_version = kwargs.get("tls_version", "")
        self.debug = kwargs.get("debug", False)

        if self.debug:
            Logger.info("VOIP: Starting call")
        self.verify_permission()
        if self.hasPermission:
            self.connected = False
            if self.debug:
                Logger.info(f"VOIP: {timeout} sec(s) wait for connection")
            self.processor.connect_port_ssl_tlsVersion_timeout_(
                dst_address, dst_port, ssl, tls_version, timeout
            )
            if self.processor.connected():
                if self.debug:
                    Logger.info(f"VOIP: Connected to {dst_address}:{dst_port}")
                self.connected = True
                self.active_call = True
                if client_id != "":
                    self.processor.sendClientID_(client_id)
                self.configure_audio_session()
                self.start_audio_engine()
                threading.Thread(
                    target=self.track_call_activity, daemon=True
                ).start()
            else:
                if self.debug:
                    Logger.error(
                        "VOIP: Could not connect to "
                        f"{dst_address}:{dst_port}. "
                        "Ensure server is reachable."
                    )

    def track_call_activity(self):
        while self.processor.callActive:
            pass
        if self.debug:
            Logger.info("VOIP: Audio stream ended.")
        self.active_call = False

    def start_audio_engine(self):
        self.input_node = self.audio_engine.inputNode
        self.audio_engine.attachNode_(self.player_node)
        self.audio_engine.connect_to_format_(
            self.player_node,
            self.audio_engine.mainMixerNode,
            self.processor.inputAudioFormat,
        )
        self.audio_engine.prepare()
        try:
            self.audio_engine.startAndReturnError_(None)
            self.player_node.play()
            self.processor.receiveAudioData()
            audioFrames = int(self.buffersize / (16 / 8 * self.channels))
            self.processor.installTapOnBus_bufferSize_(
                self.input_node, audioFrames
            )
            if self.debug:
                Logger.info("VOIP: Audio engine started successfully.")
                Logger.info("VOIP: Streaming audio")
        except Exception as e:
            if self.debug:
                Logger.error(f"VOIP: Failed to start audio engine: {e}")

    def _end_call(self):
        if self.debug:
            Logger.info("VOIP: Ending call")
        if self.connected:
            self.input_node.removeTapOnBus_(0)
            self.audio_engine.stop()
            self.player_node.stop()
            self.processor.disconnect()
        if self.debug:
            Logger.info("VOIP: Call ended")


def instance():
    return iOSVoip()
