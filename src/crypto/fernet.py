from cryptography.fernet import Fernet

from crypto.helpers import generate_key


def encrypt(text: str, passphrase: str) -> str:
    key = generate_key(passphrase)
    fernet = Fernet(key)
    encrypted_text = fernet.encrypt(text.encode())
    return encrypted_text.decode()


def decrypt(encrypted_text: str, passphrase: str) -> str:
    key = generate_key(passphrase)
    fernet = Fernet(key)
    decrypted_text = fernet.decrypt(encrypted_text.encode())
    return decrypted_text.decode()
