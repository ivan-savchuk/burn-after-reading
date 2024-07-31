import os

from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from db.sqlite_queries import get_secret_by_link, update_viewed_status


media_router = APIRouter()
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
            "dns_link": f"{os.environ.get('HOST')}:{os.environ.get('PORT')}/display-secret?hash_link={hash_link}"
        }
    )


@media_router.get("/display-secret", response_class=HTMLResponse)
def display_secret(request: Request, hash_link: str) -> templates.TemplateResponse:
    """
    localhost:8000/display-secret?hash_link=TESTING
    """
    secret = get_secret_by_link(hash_link)
    if secret.viewed:
        raise HTTPException(status_code=404, detail={"message": "Secret not found"})

    update_viewed_status(hash_link, 1)
    return templates.TemplateResponse("secret.html", {"request": request, "secret": secret.secret})
