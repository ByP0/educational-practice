from fastapi import APIRouter, Depends, HTTPException, Query, Header, Path
from typing import Annotated, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.postgres import get_session
from app.cruds.tours_cruds import get_tours_by_fort_id, delete_tour_db, add_tour_db, patch_tour_tb, register_user_to_tour, get_user_tours
from app.schemas.tours_schemas import ToursData, TourAdd, TourPatch
from app.schemas.response_schemas import Response200
from app.cruds.users_cruds import check_session


router = APIRouter(tags=["Tours"], prefix="/tours")


@router.post("/add", response_model=Response200)
async def add_tour(
    data: TourAdd,
    user_session: Annotated[str, Header(title="User session", example="123e4567-e89b-12d3-a456-426614174000")],
    session: AsyncSession = Depends(get_session),
):
    user = await check_session(user_session=user_session, session=session)
    try:
        await add_tour_db(data=data, session=session, user_id=user)
        return Response200
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error {str(e)}")
    
@router.get("/my", response_model=list[ToursData])
async def get_my_tours(
    user_session: Annotated[str, Header(title="User session", example="123e4567-e89b-12d3-a456-426614174000")],
    session: AsyncSession = Depends(get_session),
):
    user_id = await check_session(user_session=user_session, session=session)
    tours = await get_user_tours(user_id=user_id, session=session)
    return tours


@router.get("/", response_model=list[ToursData])
async def get_tours_fort(
    fort_id: Annotated[Optional[int], Query(title="Fort ID", example=1)],
    user_session: Annotated[str, Header(title="User session", example="123e4567-e89b-12d3-a456-426614174000")],
    session: AsyncSession = Depends(get_session),
):
    await check_session(user_session=user_session, session=session)
    tours = await get_tours_by_fort_id(fort_id=fort_id, session=session)
    return tours


@router.delete("/delete", response_model=Response200)
async def delete_tour(
    tour_id: Annotated[Optional[int], Query(title="Fort ID", example=1)],
    user_session: Annotated[str, Header(title="User session", example="123e4567-e89b-12d3-a456-426614174000")],
    session: AsyncSession = Depends(get_session),
):
    await check_session(user_session=user_session, session=session)
    await delete_tour_db(tour_id=tour_id, session=session)
    return Response200(detail="Succesful deleted")
    

@router.patch("/patch", response_model=Response200)
async def patch_tour(
    new_data: TourPatch,
    tour_id: Annotated[Optional[int], Query(title="Fort ID", example=1)],
    user_session: Annotated[str, Header(title="User session", example="123e4567-e89b-12d3-a456-426614174000")],
    session: AsyncSession = Depends(get_session),
):
    await check_session(user_session=user_session, session=session)
    await patch_tour_tb(tour_id=tour_id, data=new_data, session=session)
    return Response200


@router.post("/{tour_id}/register", response_model=Response200)
async def register_to_tour(
    tour_id: Annotated[int, Path(title="Tour ID", example=1)],
    user_session: Annotated[str, Header(title="User session", example="123e4567-e89b-12d3-a456-426614174000")],
    session: AsyncSession = Depends(get_session),
):
    user_id = await check_session(user_session=user_session, session=session)
    await register_user_to_tour(user_id=user_id, tour_id=tour_id, session=session)
    return Response200