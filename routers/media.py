from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


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
            "hash_link": hash_link
        }
    )
