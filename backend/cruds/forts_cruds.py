from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from backend.models.models import Forts
from backend.services.users_services import hash_password


async def get_forts(session: AsyncSession):
    stmt = select(Forts)
    result: Result = await session.execute(stmt)
    return result.scalars().all()
