from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from fastapi import HTTPException
import uuid

from app.models.models import Users, Sessions
from app.schemas.users_schemas import UserSchema


async def add_session(user_id: int, session: AsyncSession) -> str:
    user_session = str(uuid.uuid4())
    data_for_db = Sessions(session=user_session, user_id=user_id)
    session.add(data_for_db)
    await session.commit()
    await session.refresh(data_for_db)
    return user_session

async def check_session(user_session: str, session: AsyncSession) -> int:
    try:
        stmt = select(Sessions).where(Sessions.session == user_session)
        result: Result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=401, detail="Not authorized")
        return user.user_id
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_user_by_session(user_session: str, session: AsyncSession) -> UserSchema:
    try:
        stmt = select(Sessions.user_id).where(Sessions.session == user_session)
        session_result: Result = await session.execute(stmt)
        user_id = session_result.scalar_one_or_none()
        if user_id:
            user_stmt = select(Users).where(Users.user_id == user_id)
            user_result: Result = await session.execute(user_stmt)
            user_db = user_result.scalar_one_or_none()
            return UserSchema(
                first_name=user_db.first_name,
                last_name=user_db.last_name,
                patronymic=user_db.patronymic,
                email=user_db.email,
                birth_date=user_db.birth_date,
                )
        else:
            raise HTTPException(status_code=401, detail="Invalid session")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))