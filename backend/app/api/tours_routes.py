from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.postgres import get_session
from app.cruds.tours_cruds import get_tours_by_fort_id, delete_tour_db, add_tour_db, patch_tour_tb
from app.schemas.tours_schemas import ToursData, TourAdd, TourPatch
from app.schemas.response_schemas import Response200


router = APIRouter(tags=["Tours"], prefix="/tours")


@router.post("/add", response_model=Response200)
async def add_tour(
    data: TourAdd,
    session: AsyncSession = Depends(get_session),
):
    try:
        await add_tour_db(data=data, session=session)
        return Response200
    except:
        raise HTTPException(status_code=500, detail="Server Error")


@router.get("/", response_model=list[ToursData])
async def get_tours_fort(
    fort_id: Annotated[Optional[int], Query(title="Fort ID", example=1)],
    session: AsyncSession = Depends(get_session),
):
    tours = await get_tours_by_fort_id(fort_id=fort_id, session=session)
    return tours


@router.delete("/delete", response_model=Response200)
async def delete_tour(
    tour_id: Annotated[Optional[int], Query(title="Fort ID", example=1)],
    session: AsyncSession = Depends(get_session),
):
    await delete_tour_db(tour_id=tour_id, session=session)
    return Response200(detail="Succesful deleted")
    

@router.patch("/patch", response_model=Response200)
async def patch_tour(
    new_data: TourPatch,
    tour_id: Annotated[Optional[int], Query(title="Fort ID", example=1)],
    session: AsyncSession = Depends(get_session),
):
    await patch_tour_tb(tour_id=tour_id, data=new_data, session=session)
    return Response200