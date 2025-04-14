from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.users_schemas import SingUpUser, SingInUser, UserSession
from backend.database.postgres import get_session
from backend.cruds.users_cruds import register_user, get_user_by_email, add_session
from backend.services.users_services import validate_password


router = APIRouter(tags=["Users"])


@router.post("/sing_up", response_model=UserSession)
async def sing_up_user(
    data: SingUpUser,
    session: AsyncSession = Depends(get_session)
    ):
    user_id = await register_user(data=data, session=session)
    user_session = await add_session(user_id=user_id, session=session)
    return UserSession(session=user_session)


@router.post("/sing_in", response_model=UserSession)
async def sing_in_user(
    data: SingInUser,
    session: AsyncSession = Depends(get_session)
    ):
    user = await get_user_by_email(email=data.email, session=session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not validate_password(data.password, user.password.encode('utf-8')):
        raise HTTPException(status_code=404, detail="Invalid password")
    user_session = await add_session(user_id=user.user_id, session=session)
    return UserSession(session=user_session)