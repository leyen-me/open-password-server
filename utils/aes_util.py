import base64
from Crypto.Cipher import AES
from constants import aes_iv

class AesUtil(object):
    
    def __init__(self, key):
        self.key = key.encode('utf-8')
        self.mode = AES.MODE_CBC
        self.iv = aes_iv.encode('utf-8')

    def encrypt(self, text):
        text = text.encode('utf-8')
        cryptor = AES.new(self.key, self.mode, self.iv)
        length = 16
        count = len(text)
        if count < length:
            add = (length - count)
            text = text + ('\0' * add).encode('utf-8')
        elif count > length:
            add = (length - (count % length))
            text = text + ('\0' * add).encode('utf-8')
        self.ciphertext = cryptor.encrypt(text)
        return base64.b64encode(self.ciphertext)

    def decrypt(self, text) -> str:
        cryptor = AES.new(self.key, self.mode, self.iv)
        plain_text = cryptor.decrypt(base64.b64decode(text))
        cleaned_byte_string = plain_text.replace(b'\x00', b'')
        return cleaned_byte_string.decode('utf-8')