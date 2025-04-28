from fastapi import APIRouter

from backend.app.api.routes import users, forts, tours

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(users)
api_router.include_router(forts)
api_router.include_router(tours)