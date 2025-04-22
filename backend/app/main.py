from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.forts_routes import router as forts_router
from app.api.users_routers import router as users_router
from app.api.tours_routes import router as tours_router
from app.database.postgres import upload_forts, get_session, create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    async with get_session() as session:
        await upload_forts(session, "app/database/data_forts")
        yield


app = FastAPI(lifespan=lifespan)


origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(forts_router)
app.include_router(users_router)
app.include_router(tours_router)