from urllib.parse import urlencode

from fastapi import APIRouter, Form, status
from fastapi.responses import RedirectResponse

from crypto.fernet import encrypt
from crypto.helpers import get_random_hash

from config.config import AppConfig
from db.crud_queries import insert_secret
from entities.secret_record import SecretRecord


db_router = APIRouter()
cfg = AppConfig().get_config()


@db_router.post("/submit-secret")
def handle_secret(secret: str = Form(), passphrase: str | None = Form(None),
                  expiration_time: str | None = Form(None)) -> RedirectResponse:

    passphrase = passphrase if passphrase else cfg.get("DEFAULT_PASSPHRASE")
    encrypted_secret = encrypt(secret, passphrase)

    secret_record = SecretRecord(
        secret=encrypted_secret,
        passphrase=passphrase,
        passphrase_applied=1 if passphrase else 0,
        expiration_datetime="7d" if not expiration_time else expiration_time,
        hash_link=get_random_hash()
    )

    insert_status = 1 if insert_secret(secret_record) else 0
    encoded_params = urlencode({"status": insert_status, "hash_link": secret_record.hash_link})
    return RedirectResponse(f"/generation-result?{encoded_params}", status_code=status.HTTP_303_SEE_OTHER)
