import json

from jnius import autoclass, cast

from plyer.facades import Keystore
from plyer.platforms.android import activity


class AndroidKeystore(Keystore):
    def _set_key(self, servicename, key, value, encrypt=True, **kwargs):
        """
        Encrypts the value using a secret key and stores it in the Android Keystore system.

        Args:
            servicename (str): The name of the service.
            key (str): The key to store the value under.
            value (str): The value to be encrypted and stored.
            encrypt (bool, optional): Whether to encrypt the value. Defaults to True.
            **kwargs: Additional keyword arguments.

        Returns:
            None
        """
        if encrypt:
            cipher, iv = self.encrypt_key(value, servicename)
            cipher, iv = self.cipher_text_wrapper(cipher, iv)
            value = json.dumps({'cipher': cipher, 'iv': iv})
        mode = kwargs.get("mode", 0)
        settings = activity.getSharedPreferences(servicename, mode)
        editor = settings.edit()
        editor.putString(key, value)
        editor.commit()

    @staticmethod
    def cipher_text_wrapper(cipher, iv):
        return ','.join([str(x) for x in cipher]), ','.join([str(x) for x in iv])

    def encrypt_key(self, value, servicename):
        """
        Encrypts the value using a secret key.

        Args:
            value (str): The value to be encrypted.
            servicename (str): The name of the service.

        Returns:
            tuple: A tuple containing the encrypted value and the initialization vector.

        https://developer.android.com/reference/android/security/keystore/KeyProperties
        https://developer.android.com/reference/javax/crypto/KeyGenerator
        https://developer.android.com/reference/android/security/keystore/KeyGenParameterSpec
        https://developer.android.com/reference/android/security/keystore/KeyGenParameterSpec.Builder
        """
        KeyProperties = autoclass('android.security.keystore.KeyProperties')
        KeyGenerator = autoclass('javax.crypto.KeyGenerator')
        KeyGenParameterSpec = autoclass('android.security.keystore.KeyGenParameterSpec$Builder')
        String = autoclass('java.lang.String')

        # Configure the KeyGenerator
        kg = KeyGenParameterSpec(servicename, KeyProperties.PURPOSE_ENCRYPT | KeyProperties.PURPOSE_DECRYPT)
        kg.setBlockModes(KeyProperties.BLOCK_MODE_GCM)
        kg.setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
        key_generator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
        key_generator.init(kg.build())

        # Generate the key
        cipher = self.get_cipher()
        cipher.init(1, cast('java.security.Key', key_generator.generateKey()))
        return cipher.doFinal(String(value).getBytes("UTF-8")), cipher.getIV()

    @staticmethod
    def get_cipher():
        """
        Returns an instance of the Cipher class.
        """
        Cipher = autoclass('javax.crypto.Cipher')
        return Cipher.getInstance("AES/GCM/NoPadding")

    def _get_key(self, servicename, key, decrypt=True, **kwargs):
        """
        Retrieves the value associated with the given key from the Android Keystore system.

        Args:
            servicename (str): The name of the service.
            key (str): The key to retrieve the value for.
            decrypt (bool, optional): Whether to decrypt the value. Defaults to True.
            **kwargs: Additional keyword arguments.

        Returns:
            str: The decrypted value associated with the key.
        """
        mode = kwargs.get("mode", 0)
        default = kwargs.get("default", "__None")
        settings = activity.getSharedPreferences(servicename, mode)
        ret = settings.getString(key, default)
        if decrypt:
            cipherTextWrapper = json.loads(ret)
            ret = self.decrypt_key(servicename, cipherTextWrapper)
        if ret == "__None":
            ret = None
        return ret

    def decrypt_key(self, servicename, cipherTextWrapper):
        """
        Decrypts the value using a secret key.

        Args:
            servicename (str): The name of the service.
            cipherTextWrapper (CipherTextWrapper): An json string containing the encrypted value and the initialization vector.

        Returns:
            str: The decrypted value.
        https://developer.android.com/reference/javax/crypto/spec/GCMParameterSpec
        Specifies the set of parameters required by a Cipher using the Galois/Counter Mode (GCM) mode.
        """
        GCMParameterSpec = autoclass('javax.crypto.spec.GCMParameterSpec')
        String = autoclass('java.lang.String')

        # Get the key and the cipher
        secretKey = self.get_secret_key(servicename)
        cipher = self.get_cipher()

        # separate the encrypted data and the initialization vector
        iv = [int(x) for x in cipherTextWrapper['iv'].split(",")]
        e = [int(x) for x in cipherTextWrapper['cipher'].split(",")]

        # decrypt the data
        cipher.init(2, secretKey, GCMParameterSpec(128, iv))
        decryptedData = cipher.doFinal(e)
        p = String(decryptedData, "UTF-8").toCharArray()
        return ''.join(p)

    @staticmethod
    def get_secret_key(servicename):
        """
        Retrieves the secret key from the Android Keystore system.

        Args:
            servicename (str): The name of the service.

        Returns:
            Key: The secret key.
        """
        KeyStore = autoclass('java.security.KeyStore')
        keyStore = KeyStore.getInstance("AndroidKeyStore")
        keyStore.load(None)
        return keyStore.getKey(servicename, None)


def instance():
    return AndroidKeystore()

