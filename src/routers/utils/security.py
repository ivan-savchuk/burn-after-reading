from fastapi import HTTPException, status, Security
from fastapi.security.api_key import APIKeyHeader

from crypto.fernet import decrypt
from config.config import AppConfig
from db.user import check_for_api_key

from entities.secret_record import SecretRecord


cfg = AppConfig().get_config()
# auto_error=True - means that it is the only method for authentication
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)


def decrypt_secret(secret: SecretRecord, passphrase: str) -> str | None:
    decrypted_secret = decrypt(
        secret.secret,
        passphrase if passphrase else cfg.get("DEFAULT_PASSPHRASE")
    )

    if not decrypted_secret:
        raise HTTPException(status_code=401, detail={"msg": "Invalid passphrase provided"})

    return decrypted_secret


def check_api_key(api_key: str = Security(api_key_header)) -> None:
    if not check_for_api_key(api_key):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"msg": "Invalid API key provided"})
