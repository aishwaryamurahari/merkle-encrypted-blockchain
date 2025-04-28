from cryptography.fernet import Fernet

class CryptoUtils:
    def __init__(self, key=None, key_file=None):
        if key_file:
            self.key = self.load_key(key_file)
        elif key:
            self.key = key
        else:
            self.key = Fernet.generate_key()
            self.save_key("key.key")  # Default save if no key provided
        self.cipher = Fernet(self.key)

    def encrypt(self, data):
        return self.cipher.encrypt(data.encode('utf-8')).decode('utf-8')

    def decrypt(self, encrypted_data):
        return self.cipher.decrypt(encrypted_data.encode('utf-8')).decode('utf-8')

    def save_key(self, filename):
        with open(filename, "wb") as file:
            file.write(self.key)

    def load_key(self, filename):
        with open(filename, "rb") as file:
            return file.read()
