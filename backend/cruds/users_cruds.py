from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from fastapi import HTTPException
import uuid

from backend.models.models import Users, Sessions
from backend.schemas.users_schemas import SingUpUser, SingInUser
from backend.services.users_services import hash_password

async def add_session(user_id: int, session: AsyncSession):
    user_session = str(uuid.uuid4())
    data_for_db = Sessions(session=user_session, user_id=user_id)
    session.add(data_for_db)
    await session.commit()
    await session.refresh(data_for_db)
    return user_session

async def check_session(user_session: str, session: AsyncSession):
    try:
        stmt = select(Sessions).where(Sessions.session == user_session)
        result: Result = await session.execute(stmt)
        return result.scalar_one()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def register_user(data: SingUpUser, session: AsyncSession):
    try:
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
        return int(data_for_db.user_id)
    except:
        raise HTTPException(status_code=409, detail="The email address is already associated with another account.")

async def get_user_by_email(email: str, session: AsyncSession):
    stmt = select(Users).where(Users.email == email)
    result: Result = await session.execute(stmt)
    return result.scalar_one()