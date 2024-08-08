from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Request, Form, status

from urllib.parse import urlencode

from core.cryptography import encrypt
from core.cryptography import get_random_hash

from core.config.config import AppConfig
from api.utils.checker import Checker
from api.utils.security import decrypt_secret
from entities.secret_record import SecretRecord
from database.crud import get_secret_by_link, update_viewed_status, insert_secret


cfg = AppConfig().get_config()
endpoints_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@endpoints_router.get("/", response_class=HTMLResponse)
def display_form_page(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse("main.html", {"request": request})


@endpoints_router.get("/generation-result", response_class=HTMLResponse)
def display_result(request: Request, status_code: int, hash_link: str) -> templates.TemplateResponse:
    return templates.TemplateResponse(
        "created.html",
        {
            "request": request,
            "status_code": status_code,
            "dns_link": f"{cfg.get('HOST')}:{cfg.get('PORT')}/request-secret?hash_link={hash_link}"
        }
    )


@endpoints_router.get("/request-secret", response_class=HTMLResponse)
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
    encoded_params = urlencode({"status_code": insert_status, "hash_link": secret_record.hash_link})
    return RedirectResponse(f"/generation-result?{encoded_params}", status_code=status.HTTP_303_SEE_OTHER)


@endpoints_router.get("/request-secret", response_class=HTMLResponse)
def request_secret(request: Request, hash_link: str) -> templates.TemplateResponse:
    secret = get_secret_by_link(hash_link)

    Checker.apply_checks(secret)

    return templates.TemplateResponse("request.html", {"request": request, "hash_link": hash_link})


@endpoints_router.post("/display-secret", response_class=HTMLResponse)
def display_secret(request: Request,
                   hash_link: str = Form(...), passphrase: str | None = Form(None)) -> templates.TemplateResponse:
    secret = get_secret_by_link(hash_link)

    Checker.apply_checks(secret)

    decrypted_secret = decrypt_secret(secret, passphrase)
    update_viewed_status(hash_link, 1)

    return templates.TemplateResponse("secret.html", {"request": request, "secret": decrypted_secret})
