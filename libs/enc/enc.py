

import base64
import secrets
import jwt
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

#private access
class EncryptAndDecryptAlgoritm():
    
    __app_secret = secrets.token_hex(16)
    __jwt_secret = secrets.token_hex(32)
    JWT_ALGORITHM = 'HS256'
    JWT_EXP_DELTA_SECONDS = 3600 * 12  # Token expires after 12 hour
    
    @staticmethod
    def generate_aes_key():
        return secrets.token_bytes(32)  # Generate a 32-byte key for AES-256

    @staticmethod
    def decrypt_data(encrypted_data, secret_key):
        encrypted_data_bytes = base64.b64decode(encrypted_data)
        cipher = AES.new(secret_key, AES.MODE_ECB)
        decrypted_data = unpad(cipher.decrypt(encrypted_data_bytes), AES.block_size)
        return decrypted_data.decode('utf-8')
    
    @classmethod
    def jwt_decode(cls, token):
        return jwt.decode(token, cls.__jwt_secret, algorithms=[cls.JWT_ALGORITHM])
    
    @classmethod
    def jwt_encode(cls, payload):
        return jwt.encode(payload, cls.__jwt_secret, cls.JWT_ALGORITHM)
    
    @classmethod
    def get_app_secret(cls):
        return cls.__app_secret
    
    @classmethod
    def get_jwt_secret(cls):
        return cls.__jwt_secret
    
