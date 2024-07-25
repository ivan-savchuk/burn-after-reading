from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


media_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@media_router.get("/", response_class=HTMLResponse)
def anon_secret(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})
