from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from api.endpoints import endpoints_router
from api.crud import crud_router


app = FastAPI()
app.include_router(endpoints_router)
app.include_router(crud_router)
