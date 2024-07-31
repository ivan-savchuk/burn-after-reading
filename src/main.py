from fastapi import FastAPI
from dotenv import load_dotenv

from routers.db import db_router
from routers.media import media_router


load_dotenv()

app = FastAPI()
app.include_router(db_router)
app.include_router(media_router)