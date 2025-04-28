from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from fastapi import HTTPException

from app.models.models import Users
from app.schemas.users_schemas import UserSchema, ChangeUserSchema
from app.utils import hash_password


async def get_user_by_id(user_id: int, session: AsyncSession) -> UserSchema:
    try:
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
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

async def change_user_db(user_id: int, data: ChangeUserSchema, session: AsyncSession):
    try:
        stmt = select(Users).where(Users.user_id == user_id)
        result: Result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        
        if data.first_name:
            user.first_name = data.first_name
        if data.last_name:
            user.last_name = data.last_name
        if data.patronymic:
            user.patronymic = data.patronymic
        if data.email:
            user.email = data.email
        if data.birth_date:
            user.birth_date = data.birth_date
        
        await session.commit()
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def update_password(user_id: int, new_password: str, session: AsyncSession):
    try:
        stmt = select(Users).where(Users.user_id == user_id)
        result: Result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        
        user.password = hash_password(new_password).decode('utf-8')
        await session.commit()

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def delete_user_db(user_id: int, session: AsyncSession):
    try:
        stmt = select(Users).where(Users.user_id == user_id)
        result: Result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        
        await session.delete(user)
        await session.commit()
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))