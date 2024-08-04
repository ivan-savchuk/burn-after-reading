from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from routers.db import db_router
from routers.media import media_router
from routers.crud import crud_router


app = FastAPI()
app.include_router(db_router)
app.include_router(media_router)
app.include_router(crud_router)
