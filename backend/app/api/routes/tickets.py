from fastapi import APIRouter, Request, Query, Depends, HTTPException
from typing import Annotated, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.response_schemas import Response200
from app.schemas.tickets_schemas import TicketsDataSchema
from app.core.security import dependencies, get_token_data
from app.cruds.tickets_cruds import create_ticket, get_user_tickets
from app.database.postgres import get_session


router = APIRouter(tags=["Tickets"], prefix="/tickets", dependencies=dependencies)


@router.get("/", response_model=list[TicketsDataSchema])
async def get_my_tickets(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    token_data = get_token_data(request=request)
    tickets = await get_user_tickets(user_id=token_data.get("user_id"), session=session)
    return tickets
    


@router.post("/", response_model=Response200)
async def buy_ticket(
    request: Request,
    tour_id: Annotated[Optional[int], Query(title="Tour ID", example=1)],
    session: AsyncSession = Depends(get_session)
):
    token_data = get_token_data(request=request)
    if not tour_id:
        raise HTTPException(status_code=422, detail="Tour ID must be provided")
    await create_ticket(user_id=token_data.get("user_id"), tour_id=tour_id, session=session)
    return Response200