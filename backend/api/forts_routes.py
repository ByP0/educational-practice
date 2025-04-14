from fastapi import APIRouter, Depends, Request, Header
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.postgres import get_session
from backend.cruds.forts_cruds import get_forts, add_fort_db
from backend.schemas.forts_schemas import FortAdd, FortsData
from backend.schemas.response_schemas import Response200
from backend.cruds.users_cruds import check_session


router = APIRouter(tags=["Forts"], prefix="/forts")


@router.get("/all")
async def get_all_forts(
    user_session: Annotated[str, Header(title="User session", example="123e4567-e89b-12d3-a456-426614174000")],
    session: AsyncSession = Depends(get_session),
):
    await check_session(user_session=user_session, session=session)
    forts_data = await get_forts(session=session)
    return forts_data


@router.post("/add", response_model=Response200)
async def add_fort(
    data: FortAdd,
    session: AsyncSession = Depends(get_session)
    ):
    await add_fort_db(data=data, session=session)
    return Response200
    


@router.post("/upload_image")
async def upload_image():
    pass