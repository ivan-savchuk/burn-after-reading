from fastapi import APIRouter, status, HTTPException, Depends

from crypto.helpers import get_random_hash
from crypto.fernet import encrypt

from entities.secret_record import SecretRecord
from entities.crud import SecretCreate, SecretDNSLink, SecretRequest, SecretData

from config.config import AppConfig
from routers.utils.checker import Checker
from routers.utils.security import decrypt_secret, check_api_key
from db.crud_queries import insert_secret, get_secret_by_link, update_viewed_status


crud_router = APIRouter()
cfg = AppConfig().get_config()


@crud_router.post("/create-secret", response_model=SecretDNSLink)
def create_secret(secret: SecretCreate, _: str = Depends(check_api_key)):

    passphrase = secret.passphrase if secret.passphrase else cfg.get("DEFAULT_PASSPHRASE")
    encrypted_secret = encrypt(secret.secret, passphrase)

    secret_record = SecretRecord(
        secret=encrypted_secret,
        passphrase=passphrase,
        passphrase_applied=1 if passphrase else 0,
        expiration_datetime=secret.expiration_time.value,
        hash_link=get_random_hash()
    )

    insert_status = 1 if insert_secret(secret_record) else 0
    if insert_status:
        return SecretDNSLink(
            dns_html_link=f"{cfg.get('HOST')}:{cfg.get('PORT')}/request-secret?hash_link={secret_record.hash_link}",
            dns_api_link=f"{cfg.get('HOST')}:{cfg.get('PORT')}/secret/{secret_record.hash_link}"
        )

    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create secret")


@crud_router.post("/secret/{hash_link}", response_model=SecretData)
def read_secret(hash_link: str, secret_request: SecretRequest, _: str = Depends(check_api_key)):
    secret = get_secret_by_link(hash_link)

    Checker.apply_checks(secret)

    decrypted_secret = decrypt_secret(secret, secret_request.passphrase)
    update_viewed_status(hash_link, 1)

    return SecretData(secret=decrypted_secret)


@crud_router.post("/secret/burn/{hash_link}", status_code=status.HTTP_204_NO_CONTENT)
def burn_secret(hash_link: str, secret_request: SecretRequest | None = None, _: str = Depends(check_api_key)):
    secret = get_secret_by_link(hash_link)

    Checker.apply_checks(secret)

    _ = decrypt_secret(secret, secret_request.passphrase)
    update_viewed_status(hash_link, 1)

    return None
