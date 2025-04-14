from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from backend.models.models import Tours
from backend.schemas.tours_schemas import ToursData, TourAdd


async def get_tours_by_fort_id(fort_id: int, session: AsyncSession) -> list[ToursData]:
    stmt = select(Tours).where(Tours.fort_id==fort_id)
    result: Result = await session.execute(stmt)
    return [ToursData(
        tour_id=tour.tour_id,
        gathering_place=tour.gathering_place,
        tour_date=tour.tour_date,
        number_of_seats=tour.number_of_seats,
        fort_id=tour.fort_id
        )
        for tour in result]

async def delete_tour_db(tour_id: int, session: AsyncSession):
    stmt = select(Tours).where(Tours.tour_id==tour_id)
    await session.delete(stmt)
    await session.commit()

async def add_tour_db(data: TourAdd, session: AsyncSession):
    data_for_db = Tours(
        gathering_place=data.gathering_place,
        tour_date=data.tour_date,
        number_of_seats=data.number_of_seats,
        fort_id=data.fort_id
    )
    session.add(data_for_db)
    await session.commit()
    await session.refresh(data_for_db)
    