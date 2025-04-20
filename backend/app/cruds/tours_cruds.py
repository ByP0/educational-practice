from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from fastapi import HTTPException

from app.models.models import Tours
from app.schemas.tours_schemas import ToursData, TourAdd, TourPatch


async def get_tours_by_fort_id(fort_id: int, session: AsyncSession) -> list[ToursData]:
    stmt = select(Tours).where(Tours.fort_id==fort_id)
    result: Result = await session.execute(stmt)
    tours = result.scalars().all()
    return [ToursData(
        tour_id=tour.tour_id,
        gathering_place=tour.gathering_place,
        tour_date=tour.tour_date,
        number_of_seats=tour.number_of_seats,
        fort_id=tour.fort_id
        )
        for tour in tours]

async def delete_tour_db(tour_id: int, session: AsyncSession):
    stmt = select(Tours).where(Tours.tour_id == tour_id)
    result: Result = await session.execute(stmt)
    tour = result.scalar_one_or_none()

    if tour is None:
        raise HTTPException(status_code=404, detail="Tour not found")

    await session.delete(tour)
    await session.commit()

async def add_tour_db(data: TourAdd, session: AsyncSession, user_id: int):
    data_for_db = Tours(
        gathering_place=data.gathering_place,
        tour_date=data.tour_date,
        number_of_seats=data.number_of_seats,
        fort_id=data.fort_id,
        user_id=user_id,
    )
    session.add(data_for_db)
    await session.commit()
    await session.refresh(data_for_db)
    
async def patch_tour_tb(tour_id: int, data: TourPatch, session: AsyncSession):
    stmt = select(Tours).where(Tours.tour_id == tour_id)
    
    result: Result = await session.execute(stmt)
    tour = result.scalar_one_or_none()
    
    if tour is None:
        raise HTTPException(status_code=404, detail=f"Tour with id {tour_id} not found.")

    if data.fort_id is not None:
        tour.fort_id = data.fort_id
    if data.gathering_place is not None:
        tour.gathering_place = data.gathering_place
    if data.tour_date is not None:
        tour.tour_date = data.tour_date
    if data.number_of_seats is not None:
        tour.number_of_seats = data.number_of_seats
    
    await session.commit()