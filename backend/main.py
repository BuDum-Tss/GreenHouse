import os.path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.depends import DB_FILENAME
from src.api import user, recommendation, dishes, cart
from src.db import init_db

app = FastAPI(
    title="GreenHouse API",
    version="0.1.0"
)

@app.on_event("startup")
def on_startup():
    if not os.path.exists(DB_FILENAME):
        init_db()

# Разрешение CORS для сайта
origins = [
    "https://greenhouse-nu.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user)
app.include_router(recommendation)
app.include_router(dishes)
app.include_router(cart.router)
