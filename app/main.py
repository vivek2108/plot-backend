from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.api import auth_router, buyers, users
from app.config.database import Base, engine

app = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=1400)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(buyers.router, prefix="/buyers", tags=["buyers"])

Base.metadata.create_all(bind=engine)
