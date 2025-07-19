import os.path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from log import setup_logging
from src.depends import ALLOW_ORIGINS, DB_FILENAME
from src.api.dishes import router as dishes
from src.api.cart import router as cart
from src.db import init_db

app = FastAPI(
    title="GreenHouse API",
    version="0.1.0"
)

@app.on_event("startup")
def on_startup():
    setup_logging()
    if not os.path.exists(DB_FILENAME):
        init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOW_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dishes)
app.include_router(cart)
