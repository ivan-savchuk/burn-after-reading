from hashlib import sha256
from base64 import urlsafe_b64encode


def generate_key(passphrase: str) -> bytes:
    # Use SHA-256 to hash the passphrase and generate a 32-byte key
    return urlsafe_b64encode(sha256(passphrase.encode()).digest())


def get_hash32(text: str):
    hash_object = sha256(text.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig[:32]
