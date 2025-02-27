'''
Android Voip
'''

from jnius import autoclass, JavaException
from plyer.facades import Voip
from kivy.logger import Logger
import threading

AudioRecord = autoclass("android.media.AudioRecord")
AudioSource = autoclass("android.media.MediaRecorder$AudioSource")
AudioFormat = autoclass("android.media.AudioFormat")
AudioTrack = autoclass("android.media.AudioTrack")
AudioManager = autoclass("android.media.AudioManager")
Socket = autoclass("java.net.Socket")
SSLSocket = autoclass("javax.net.ssl.SSLSocketFactory")
SocketTimer = autoclass("java.net.InetSocketAddress")
SSLContext = autoclass("javax.net.ssl.SSLContext")
SecureRandom = autoclass("java.security.SecureRandom")


class AndroidVoip(Voip):
    SAMPLE_RATE = 16000
    CHANNEL_CONFIG = AudioFormat.CHANNEL_IN_MONO
    AUDIO_FORMAT = AudioFormat.ENCODING_PCM_16BIT
    socket = None
    connected = False
    hasPermission = False
    data_output_stream = None
    data_input_stream = None
    audio_record = None
    active_call = False
    buffer_size = 640
    debug = False

    def __init__(self):
        min_buffer_size = AudioRecord.getMinBufferSize(
            self.SAMPLE_RATE, self.CHANNEL_CONFIG, self.AUDIO_FORMAT
        )
        if min_buffer_size > self.buffer_size:
            self.buffer_size = min_buffer_size

    def send_client_id(self, client_id):
        try:
            self.data_output_stream.write(client_id.encode())
            self.data_output_stream.flush()
            if self.debug:
                Logger.info("VOIP: Client ID sent")
        except JavaException as e:
            if self.debug:
                Logger.info("VOIP: Client ID delivery failed")
                Logger.error(f"VOIP: {e}")

    def _start_call(self, **kwargs):
        dst_address = kwargs.get('dst_address')
        dst_port = kwargs.get('dst_port')
        client_id = kwargs.get('client_id', '')
        timeout = kwargs.get('timeout', 5) * 1000
        ssl = kwargs.get('ssl', False)
        tls_version = kwargs.get('tls_version', '')
        self.debug = kwargs.get('debug', False)

        if self.debug:
            Logger.info("VOIP: Starting call")
        self.verifyPermission()
        if self.hasPermission:
            self.connected = False
            if self.debug:
                Logger.info(f"VOIP: {timeout} sec(s) wait for connection")
            try:
                if ssl:
                    if tls_version == "":
                        ssl_socket_factory = SSLSocket.getDefault()
                    else:
                        ssl_context = SSLContext.getInstance(tls_version)
                        ssl_context.init(None, None, SecureRandom())
                        ssl_socket_factory = ssl_context.getSocketFactory()
                    self.socket = ssl_socket_factory.createSocket()
                else:
                    self.socket = Socket()
                self.socket.connect(
                    SocketTimer(dst_address, dst_port),
                    timeout
                )
                self.socket.setSoTimeout(timeout)
                self.data_input_stream = self.socket.getInputStream()
                self.data_output_stream = self.socket.getOutputStream()
                self.connected = True
                if self.debug:
                    Logger.info(f"VOIP: Connected to {dst_address}:{dst_port}")
            except JavaException as e:
                if self.debug:
                    Logger.error(
                        "VOIP: "
                        "Ensure INTERNET and ACCESS_NETWORK_STATE permissions "
                        "are in buildozer.spec and server is available."
                    )
                    Logger.error(f"VOIP: {e}")
            if self.connected:
                self.active_call = True
                if client_id != "":
                    self.send_client_id(client_id)
                self.record_thread = threading.Thread(
                    target=self.send_audio, daemon=True
                )
                self.record_thread.start()
                self.listening_thread = threading.Thread(
                    target=self.receive_audio, daemon=True
                )
                self.listening_thread.start()

    def _end_call(self):
        if self.debug:
            Logger.info("VOIP: Ending call")
        self.active_call = False
        if hasattr(self, "record_thread") and self.record_thread.is_alive():
            self.record_thread.join()
        if (hasattr(self, "listening_thread") and
                self.listening_thread.is_alive()):
            self.listening_thread.join()
        if self.socket is not None:
            self.socket.close()
            self.socket = None
        if self.debug:
            Logger.info("VOIP: Call ended")

    def verifyPermission(self):
        self.hasPermission = False
        self.audio_record = AudioRecord(
            AudioSource.VOICE_COMMUNICATION,
            self.SAMPLE_RATE,
            self.CHANNEL_CONFIG,
            self.AUDIO_FORMAT,
            self.buffer_size,
        )
        if self.audio_record.getState() != AudioRecord.STATE_UNINITIALIZED:
            self.hasPermission = True
            if self.debug:
                Logger.info("VOIP: Microphone permission granted")
        else:
            if self.debug:
                Logger.error(
                    "VOIP: Permission Error: Ensure RECORD_AUDIO (Mic) "
                    "permission is enabled in app settings"
                )

    def send_audio(self):
        audio_data = bytearray(self.buffer_size)
        self.audio_record.startRecording()
        if self.debug:
            Logger.info("VOIP: Microphone live stream started")
        while self.active_call is True:
            try:
                bytes_read = self.audio_record.read(
                    audio_data, 0, self.buffer_size
                )
                if (
                    bytes_read != AudioRecord.ERROR_INVALID_OPERATION
                    and bytes_read != AudioRecord.ERROR_BAD_VALUE
                ):
                    self.data_output_stream.write(audio_data, 0, bytes_read)
                elif bytes_read == AudioRecord.ERROR_INVALID_OPERATION:
                    if self.debug:
                        Logger.warning(
                            "VOIP: ERROR_INVALID_OPERATION on microphone"
                        )
                else:
                    if self.debug:
                        Logger.warning("VOIP: ERROR_BAD_VALUE on microphone")
            except JavaException as e:
                self.active_call = False
                if self.debug:
                    Logger.error("VOIP: Microphone Stream Error")
                    Logger.error(f"VOIP: {e}")

        self.audio_record.stop()
        if self.debug:
            Logger.info("VOIP: Microphone live stream ended")

    def receive_audio(self):
        audio_track = AudioTrack(
            AudioManager.STREAM_VOICE_CALL,
            self.SAMPLE_RATE,
            AudioFormat.CHANNEL_OUT_MONO,
            self.AUDIO_FORMAT,
            self.buffer_size,
            AudioTrack.MODE_STREAM,
        )
        buffer = bytearray(self.buffer_size)
        audio_track.play()
        if self.debug:
            Logger.info("VOIP: Speaker live stream started")
        try:
            while self.active_call is True:
                bytes_received = self.data_input_stream.read(buffer)
                if bytes_received > 0:
                    audio_track.write(buffer, 0, bytes_received)
        except JavaException as e:
            self.active_call = False
            if self.debug:
                Logger.error("VOIP: Speaker Stream Error")
                Logger.error(f"VOIP: {e}")

        audio_track.stop()
        if self.debug:
            Logger.info("VOIP: Speaker live stream ended")


def instance():
    return AndroidVoip()
