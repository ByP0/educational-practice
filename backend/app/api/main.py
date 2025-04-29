from fastapi import APIRouter

from app.api.routes import users, forts, tours, tickets, auth

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(forts.router)
api_router.include_router(tours.router)
api_router.include_router(tickets.router)