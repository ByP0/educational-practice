from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.forts_routes import router as forts_router
from app.api.users_routers import router as users_router
from app.api.tours_routes import router as tours_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(forts_router)
app.include_router(users_router)
app.include_router(tours_router)