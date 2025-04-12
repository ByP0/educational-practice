from fastapi import FastAPI
from contextlib import asynccontextmanager

from backend.api.forts_routes import router as forts_router
from backend.api.users_routers import router as users_router
from backend.api.tours_routes import router as tours_router
from backend.database.postgres import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(forts_router)
app.include_router(users_router)
app.include_router(tours_router)