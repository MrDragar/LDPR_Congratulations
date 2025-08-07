import os
import uuid
from typing import Annotated

from pydantic import BaseModel
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники временно
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]  
)


@app.get("/ping")
async def ping():
    return {"message": "Pong"}


@app.get("/")
async def send_hello(request: Request):
    return {"status": "Success", "message": f"Hello"}


@app.on_event("startup")
async def startup_event():
    ...   


