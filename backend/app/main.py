from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.main import api_router
from app.database.postgres import upload_forts, create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await upload_forts("app/database/data_forts")
    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)