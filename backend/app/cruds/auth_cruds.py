from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from fastapi import HTTPException
import uuid

from app.schemas.auth_schemas import RegisterUser, LoginUser
from app.models.models import Users
from app.utils import hash_password


async def register_user_to_db(data: RegisterUser, session: AsyncSession) -> int:
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
        raise HTTPException(status_code=400, detail="The email address is already associated with another account.")
    
async def get_user_by_email(email: str, session: AsyncSession):
    stmt = select(Users).where(Users.email == email)
    result: Result = await session.execute(stmt)
    return result.scalar_one_or_none() 