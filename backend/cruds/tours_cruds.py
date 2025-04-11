from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from backend.models.models import Tours
from backend.schemas.tours_schemas import ToursData
from backend.services.users_services import hash_password


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