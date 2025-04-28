from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.schemas.auth_schemas import TokenPair, RegisterUser, LoginUser
from app.database.postgres import get_session
from app.cruds.auth_cruds import register_user_to_db, get_user_by_email
from app.core.security import set_token_pair
from app.utils import validate_password
from app.config import example_jwt_token



router = APIRouter(tags=["Auth"])


@router.post("/register", response_model=TokenPair)
async def register_user(
    data: RegisterUser,
    session: AsyncSession = Depends(get_session)
):
    user_id = await register_user_to_db(data=data, session=session)
    payload = {
        "sub": user_id,
        "email": data.email,
    }
    jwt_tokens = set_token_pair(payload)
    return TokenPair(
        access_token=jwt_tokens.get("access_token"),
        refresh_token=jwt_tokens.get("refresh_token")
    )


@router.post("/login", response_model=TokenPair)
async def login_user(
    data: LoginUser,
    session: AsyncSession = Depends(get_session),
):
    user = await get_user_by_email(email=data.email, session=session)
    validate_password(data.password, user.password.encode('utf-8'))
    payload = {
        "sub": user.user_id,
        "email": user.email,
    }
    jwt_tokens = set_token_pair(payload)
    return TokenPair(
        access_token=jwt_tokens.get("access_token"),
        refresh_token=jwt_tokens.get("refresh_token")
    )

@router.post("/token/refresh")
async def refresh_tokens(
    refresh_token: Annotated[str, Header(title="Refresh JWT-token", example=example_jwt_token)],
    session: AsyncSession = Depends(get_session),
):
    pass