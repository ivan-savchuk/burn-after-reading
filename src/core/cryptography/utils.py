from time import time
from hashlib import sha256
from secrets import token_bytes
from base64 import urlsafe_b64encode


def generate_key(passphrase: str) -> bytes:
    # Use SHA-256 to hash the passphrase and generate a 32-byte key
    return urlsafe_b64encode(sha256(passphrase.encode()).digest())


def get_random_hash() -> str:
    # Generate a random 32-byte hash
    random_bytes = token_bytes(32)
    # Use the current timestamp as a salt
    timestamp = str(time()).encode()
    return sha256(random_bytes + timestamp).hexdigest()
