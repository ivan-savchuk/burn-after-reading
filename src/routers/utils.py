from datetime import datetime

from fastapi import HTTPException

from crypto.fernet import decrypt
from config.config import AppConfig

from entities.secret_record import SecretRecord


cfg = AppConfig().get_config()


class Checker:

    @staticmethod
    def _raise_if_viewed(secret: SecretRecord) -> None:
        if secret.viewed:
            raise HTTPException(status_code=404, detail={"msg": "Secret not found"})

    @staticmethod
    def _raise_if_burned(secret: SecretRecord) -> None:
        if secret.burned:
            raise HTTPException(status_code=404, detail={"msg": "Secret has been burned"})

    @staticmethod
    def _raise_if_expired(secret: SecretRecord) -> None:
        if secret.get_expiration_datetime() < datetime.now():
            raise HTTPException(status_code=404, detail={"msg": "Secret has expired"})

    @classmethod
    def apply_checks(cls, secret: SecretRecord) -> None:
        cls._raise_if_viewed(secret)
        cls._raise_if_burned(secret)
        cls._raise_if_expired(secret)


def decrypt_secret(secret: SecretRecord, passphrase: str) -> str | None:
    decrypted_secret = decrypt(
        secret.secret,
        passphrase if passphrase else cfg.get("DEFAULT_PASSPHRASE")
    )

    if not decrypted_secret:
        raise HTTPException(status_code=401, detail={"msg": "Invalid passphrase provided"})

    return decrypted_secret
