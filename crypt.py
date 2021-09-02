from cryptography.fernet import Fernet
import base64

class crypt:

    def __init__(self):

        pass

    def encrypt_message(self, message, key, reg):
        if reg == 0:
            key = key.encode("ascii")
            key = base64.b64decode(key)
            key = key.decode("ascii") 
            key = key.encode()
            encoded_message = message.encode()
            f = Fernet(key)
            encrypted_message = f.encrypt(encoded_message) 
            return encrypted_message.decode()
        else:
            key = key.encode()
            encoded_message = message.encode()
            f = Fernet(key)
            encrypted_message = f.encrypt(encoded_message) 
            return encrypted_message.decode()


    def decrypt_message(self, encrypted_message, key):
        key = key.encode("ascii")
        key = base64.b64decode(key)
        key = key.decode("ascii")
        key = key.encode()
        f = Fernet(key)
        encrypted_message = encrypted_message.encode()
        decrypted_message = f.decrypt(encrypted_message)
        return decrypted_message.decode()
