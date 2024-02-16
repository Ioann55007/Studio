from typing import Union
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from pathlib import Path
from routes.router import router

app = FastAPI()

app.include_router(router)

app.mount("/static", StaticFiles(directory="static"), name="static")



