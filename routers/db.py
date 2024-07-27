from fastapi import APIRouter, Form, status
from fastapi.responses import RedirectResponse

from db.sqlite_queries import insert_secret
from entities.secret_record import SecretRecord


db_router = APIRouter()


@db_router.post("/submit-secret")
def handle_secret(secret: str = Form(...), passphrase: str | None = Form(None),
                  expiration_time: str | None = Form(None)) -> RedirectResponse:
    secret_record = SecretRecord(
        secret=secret,
        passphrase=passphrase,
        expiration_datetime="7d" if not expiration_time else expiration_time,
        hash_link="TESTING"
    )
    insert_secret(secret_record)

    return RedirectResponse("/generation-result", status_code=status.HTTP_303_SEE_OTHER)
