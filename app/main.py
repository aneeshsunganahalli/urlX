from fastapi import FastAPI, Depends
from functools import lru_cache
from typing import Annotated
from routers import url

app = FastAPI()
app.include_router(url.router)

@app.get("/")
def health_check():
    return {"API is running."}



    
    