from cryptography.fernet import Fernet, InvalidToken

from app_logger.logger import Logger
from crypto.helpers import generate_key


logger = Logger("fernet")


def encrypt(text: str, passphrase: str) -> str:
    key = generate_key(passphrase)
    fernet = Fernet(key)
    encrypted_text = fernet.encrypt(text.encode())
    return encrypted_text.decode()


def decrypt(encrypted_text: str, passphrase: str) -> str | None:
    try:
        key = generate_key(passphrase)
        fernet = Fernet(key)
        decrypted_text = fernet.decrypt(encrypted_text.encode())
        return decrypted_text.decode()
    except InvalidToken as exc:
        logger.error(f"Invalid token: {exc}")
        return None
