from fastapi import FastAPI

from routers.media import media_router


app = FastAPI()
app.include_router(media_router)
