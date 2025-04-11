from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.postgres import get_session
from backend.services.users_services import dependencies
from backend.cruds.forts_cruds import get_forts


router = APIRouter(tags=["Forts"], prefix="/forts", dependencies=dependencies)


@router.get("/all")
async def get_all_forts(
    session: AsyncSession = Depends(get_session)
):
    forts_data = await get_forts(session=session)
    return forts_data


@router.post("/add")
async def add_fort():
    pass


@router.post("/upload_image")
async def upload_image():
    pass