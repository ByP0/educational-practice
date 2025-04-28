from fastapi import APIRouter, Depends, Query, UploadFile
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.postgres import get_session
from app.cruds.forts_cruds import get_forts, add_fort_db, add_image_fort, get_one_fort
from app.schemas.forts_schemas import FortAdd, FortsData
from app.schemas.response_schemas import Response200
from app.core.security import dependencies


router = APIRouter(tags=["Forts"], prefix="/forts")


@router.get("/all", response_model=list[FortsData])
async def get_all_forts(
    session: AsyncSession = Depends(get_session),
):
    forts_data = await get_forts(session=session)
    return forts_data

@router.get("/", response_model=FortsData)
async def get_fort(
    fort_id: Annotated[int, Query(title="Fort ID", example=5)],
    session: AsyncSession = Depends(get_session),
):
    fort = await get_one_fort(fort_id=fort_id, session=session)
    return fort


@router.post("/add", response_model=Response200, dependencies=dependencies)
async def add_fort(
    data: FortAdd,
    session: AsyncSession = Depends(get_session)
    ):
    await add_fort_db(data=data, session=session)
    return Response200
    

@router.post("/upload_image", response_model=Response200, dependencies=dependencies)
async def upload_image(
    fort_id: Annotated[int, Query(title="Fort ID", example=1)],
    image: UploadFile,
    session: AsyncSession = Depends(get_session)
):
    await add_image_fort(fort_id=fort_id, image=image, session=session)
    return Response200