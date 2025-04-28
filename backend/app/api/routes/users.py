from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.users_schemas import SingUpUser, SingInUser, UserSession, UserSchema
from app.database.postgres import get_session
from app.cruds.users_cruds import get_user_by_session
from app.cruds.users_cruds import check_session


router = APIRouter(tags=["Users"])



@router.get("/me", response_model=UserSchema)
async def get_user(
    user_session: Annotated[str, Header(title="User session", example="123e4567-e89b-12d3-a456-426614174000")],
    session: AsyncSession = Depends(get_session)
):
    await check_session(user_session=user_session, session=session)
    user = await get_user_by_session(user_session=user_session, session=session)
    return user