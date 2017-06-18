from jnius import autoclass
from plyer.facades import Fingerprint
from plyer.platforms.android import activity
from jnius import PythonJavaClass
from jnius import java_method
from jnius import cast
from jnius import JavaClass
from jnius import MetaJavaClass
import traceback

Context = autoclass('android.content.Context')
KeyguardManager = autoclass('android.app.KeyguardManager')
FingerprintManager = autoclass(
    'android.hardware.fingerprint.FingerprintManager')
KeyStore = autoclass('java.security.KeyStore')
KeyGenerator = autoclass('javax.crypto.KeyGenerator')
KeyProperties = autoclass('android.security.keystore.KeyProperties')
NoSuchAlgorithmException = autoclass('java.security.NoSuchAlgorithmException')
NoSuchProviderException = autoclass('java.security.NoSuchProviderException')
KeyGenParameterSpecBuilder = autoclass(
    'android.security.keystore.KeyGenParameterSpec$Builder')
InvalidAlgorithmParameterException = autoclass(
    'java.security.InvalidAlgorithmParameterException')
CertificateException = autoclass('java.security.cert.CertificateException')
KeyPermanentlyInvalidatedException = autoclass(
    'android.security.keystore.KeyPermanentlyInvalidatedException')
InvalidKeyException = autoclass('java.security.InvalidKeyException')
KeyStoreException = autoclass('java.security.KeyStoreException')
UnrecoverableKeyException = autoclass(
    'java.security.UnrecoverableKeyException')
Cipher = autoclass('javax.crypto.Cipher')
NoSuchPaddingException = autoclass('javax.crypto.NoSuchPaddingException')
SecretKey = autoclass('javax.crypto.SecretKey')
CancellationSignal = autoclass('android.os.CancellationSignal')
AuthenticationResult = autoclass(
    'android.hardware.fingerprint.FingerprintManager$AuthenticationResult')
FingerprintManagerCryptoObject = autoclass(
    'android.hardware.fingerprint.FingerprintManager$CryptoObject')


class FingerprintHandler(JavaClass):
    __javaclass__ =\
        'android/hardware/fingerprint/FingerprintManager$AuthenticationCallback'
    __metaclass__ = MetaJavaClass

    def start_auth(self, fmanager, crypto_object):
            self.authentication_result = AuthenticationResult()
            self.cancellation_signal = CancellationSignal()
            fmanager.authenticate(
                crypto_object, cancellation_signal, 0, self, None)
            return self.result

    @java_method('()V')
    def onAuthenticationFailed(self):
        self.result = False

    @java_method(
        '(Landroid/hardware/fingerprint/FingerprintManager$AuthenticationResult;)V')
    def onAuthenticationSucceeded(self, authentication_result):
        self.result = True


class AndroidFingerprint(Fingerprint):
    '''
    Make sure that these requirements have been met before attempting to seek
    fingerprint authentication.

    1. A backup screen unlocking method should be configured (in other words a
       PIN or other authentication method can be used as an alternative to
       fingerprint authentication to unlock the screen).

    2. At least one fingerprint should be enrolled on the device.

    3. The app should request the USE_FINGERPRINT permission in buildozer.spec.
    '''
    def __init__(self):
        super(AndroidFingerprint, self).__init__()
        self.keyguard_manager = cast('android.app.KeyguardManager',
                    activity.getSystemService(Context.KEYGUARD_SERVICE))
        self.fingerprint_manager = cast(
                    'android.hardware.fingerprint.FingerprintManager',
                    activity.getSystemService(Context.FINGERPRINT_SERVICE))

    def _authenticate(self):
        if self.keyguard_manager.isKeyguardSecure() and\
            self._check_hardware() and self._is_enrolled():
                self.KEY_NAME = 'example_key'
                self.generate_key()
                if self.cipher_init():
                    self.crypto_object = FingerprintManagerCryptoObject(
                        self.cipher)
                    self.fingerprint_handler = FingerprintHandler()
                    result = self.fingerprint_handler.start_auth(
                        self.fingerprint_manager, self.crypto_object)
                    return result

    def _check_hardware(self):
        return self.fingerprint_manager.isHardwareDetected()

    def _is_enrolled(self):
        return self.fingerprint_manager.hasEnrolledFingerprints()

    def generate_key(self):
        try:
            self.keystore = KeyStore.getInstance('AndroidKeyStore')
        except Exception:
            traceback.print_exc()

        try:
            self.keygenerator = KeyGenerator.getInstance(
                KeyProperties.KEY_ALGORITHM_AES, 'AndroidKeyStore')
        except (NoSuchProviderException, NoSuchAlgorithmException):
            traceback.print_exc()
            raise RuntimeError('Failed to get KeyGenerator instance')

        try:
            self.keystore.load(None)
            key_type = KeyGenParameterSpecBuilder(
                self.KEY_NAME,
                KeyProperties.PURPOSE_ENCRYPT or
                KeyProperties.PURPOSE_DECRYPT).setBlockModes(
                    KeyProperties.BLOCK_MODE_CBC).setUserAuthenticationRequired(
                        True).setEncryptionPaddings(
                            KeyProperties.ENCRYPTION_PADDING_PKCS7).build()
            self.keygenerator.init(key_type)
            self.keygenerator.generateKey()
        except (NoSuchAlgorithmException, InvalidAlgorithmParameterException,
            CertificateException) as e:
                raise RuntimeError(e)

    def cipher_init(self):
        try:
            self.cipher = Cipher.getInstance(
                KeyProperties.KEY_ALGORITHM_AES + '/'
                + KeyProperties.BLOCK_MODE_CBC + '/'
                + KeyProperties.ENCRYPTION_PADDING_PKCS7)
        except (NoSuchAlgorithmException, NoSuchPaddingException) as e:
            traceback.print_exc()
            raise RuntimeError('Failed to get Cipher')

        try:
            self.keystore.load(None)
            key = self.keystore.getKey(self.KEY_NAME, None)
            self.cipher.init(Cipher.ENCRYPT_MODE, key)
            return True
        except KeyPermanentlyInvalidatedException:
            return False
        except (
            KeyStoreException,
            CertificateException,
            UnrecoverableKeyException,
            NoSuchAlgorithmException,
            InvalidKeyException) as e:
                traceback.print_exc()
                raise RuntimeError('Failed to init Cipher')


def instance():
    return AndroidFingerprint()
