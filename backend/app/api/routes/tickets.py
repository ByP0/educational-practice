from fastapi import APIRouter, Request

from app.schemas.response_schemas import Response200
from app.core.security import dependencies


router = APIRouter(tags=["Tickets"], prefix="/tickets", dependencies=dependencies)


@router.get("/")
async def get_all_tickets():
    pass