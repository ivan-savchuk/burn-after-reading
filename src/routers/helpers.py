from fastapi import HTTPException

from crypto.fernet import decrypt
from config.config import AppConfig

from entities.secret_record import SecretRecord


cfg = AppConfig().get_config()


def raise_if_viewed(secret: SecretRecord) -> None:
    if secret.viewed:
        raise HTTPException(status_code=404, detail={"msg": "Secret not found"})


def decrypt_secret(secret: SecretRecord, passphrase: str) -> str | None:
    decrypted_secret = decrypt(
        secret.secret,
        passphrase if passphrase else cfg.get("DEFAULT_PASSPHRASE")
    )

    if not decrypted_secret:
        raise HTTPException(status_code=401, detail={"msg": "Invalid passphrase provided"})

    return decrypted_secret
