from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, HTTPException, Form

from crypto.fernet import decrypt
from config.config import AppConfig
from routers.helpers import raise_if_viewed
from db.sqlite_queries import get_secret_by_link, update_viewed_status


media_router = APIRouter()
cfg = AppConfig().get_config()
templates = Jinja2Templates(directory="templates")


@media_router.get("/", response_class=HTMLResponse)
def display_form_page(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse("main.html", {"request": request})


@media_router.get("/generation-result", response_class=HTMLResponse)
def display_result(request: Request, status: int, hash_link: str) -> templates.TemplateResponse:
    return templates.TemplateResponse(
        "created.html",
        {
            "request": request,
            "status": status,
            "dns_link": f"{cfg.get('HOST')}:{cfg.get('PORT')}/request-secret?hash_link={hash_link}"
        }
    )


@media_router.get("/request-secret", response_class=HTMLResponse)
def request_secret(request: Request, hash_link: str) -> templates.TemplateResponse:
    secret = get_secret_by_link(hash_link)
    raise_if_viewed(secret)
    return templates.TemplateResponse("request.html", {"request": request, "hash_link": hash_link})


@media_router.post("/display-secret", response_class=HTMLResponse)
def display_secret(request: Request,
                   hash_link: str = Form(...), passphrase: str | None = Form(None)) -> templates.TemplateResponse:
    secret = get_secret_by_link(hash_link)
    raise_if_viewed(secret)

    decrypted_secret = decrypt(secret.secret, passphrase if passphrase else cfg.get("DEFAULT_PASSPHRASE"))
    if not decrypted_secret:
        raise HTTPException(status_code=401, detail={"message": "Invalid passphrase provided"})

    update_viewed_status(hash_link, 1)
    return templates.TemplateResponse("secret.html", {"request": request, "secret": decrypted_secret})
