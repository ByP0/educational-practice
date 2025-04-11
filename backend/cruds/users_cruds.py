from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from backend.models.models import Users
from backend.schemas.users_schemas import SingUpUser, SingInUser
from backend.services.users_services import hash_password


async def register_user(data: SingUpUser, session: AsyncSession):
    data_for_db = Users(first_name=data.first_name,
                    last_name=data.last_name, 
                    patronymic=data.patronymic, 
                    email=data.email, 
                    password=hash_password(data.password).decode('utf-8'), 
                    birth_date=data.birth_date
                )
    session.add(data_for_db)
    await session.commit()
    await session.refresh(data_for_db)
    return data_for_db.user_id

async def get_user_by_email(email: str, session: AsyncSession):
    stmt = select(Users).where(Users.email == email)
    result: Result = await session.execute(stmt)
    return result.scalar_one()