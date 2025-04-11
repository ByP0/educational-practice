from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.users_schemas import SingUpUser, SingInUser,TokenPair
from backend.database.postgres import get_session
from backend.cruds.users_cruds import register_user, get_user_by_email
from backend.services.users_services import sign_jwt, sing_refresh_jwt, validate_password, decode_refresh_jwt
from backend.config import example_jwt_token


router = APIRouter(tags=["Users"])


@router.post("/refresh", response_model=TokenPair)
async def refresh_token(
        refresh_token: Annotated[str, Header(
            title='Refresh JWT токен',
            example=example_jwt_token,
        )],
):
    token_data = decode_refresh_jwt(token=refresh_token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return TokenPair(access_token=sign_jwt(data=token_data.get("sub")),
                     refresh_token=sing_refresh_jwt(data=token_data.get("sub")))


@router.post("/sing_up", response_model=TokenPair)
async def sing_up_user(
    data: SingUpUser,
    session: AsyncSession = Depends(get_session)
    ):
    user_id = await register_user(data=data, session=session)
    return TokenPair(access_token=sign_jwt(user_id),
                     refresh_token=sing_refresh_jwt(user_id))


@router.post("/sing_in", response_model=TokenPair)
async def sing_in_user(
    data: SingInUser,
    session: AsyncSession = Depends(get_session)
    ):
    user = await get_user_by_email(email=data.email, session=session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not validate_password(data.password, user.password.encode('utf-8')):
        raise HTTPException(status_code=404, detail="Invalid password")
    return TokenPair(access_token=sign_jwt(user.user_id),
                     refresh_token=sing_refresh_jwt(user.user_id))