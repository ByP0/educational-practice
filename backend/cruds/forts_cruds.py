from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result

from backend.models.models import Forts
from backend.services.users_services import hash_password
from backend.schemas.forts_schemas import FortAdd


async def get_forts(session: AsyncSession):
    stmt = select(Forts)
    result: Result = await session.execute(stmt)
    return result.scalars().all()

async def add_fort_db(data: FortAdd, session: AsyncSession):
    data_for_db = Forts(
        fort_id=data.fort_id,
        fort_name=data.fort_name,
        description=data.description,
    )
    session.add(data_for_db)
    await session.commit()
    await session.refresh(data_for_db)

    