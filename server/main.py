from fastapi import FastAPI
from functools import lru_cache

from . import config

app = FastAPI()

@lru_cache
def get_settings():
    return config.Settings()

@app.get("/")
def read_root():
    return {"Hello": "World"}
