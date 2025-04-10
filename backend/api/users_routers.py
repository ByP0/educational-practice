from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.users_schemas import SingUpUser, TokenPair
from backend.database.postgres import get_session
from backend.cruds.users_cruds import register_user
from backend.services.users_services import sign_jwt, sing_refresh_jwt


router = APIRouter(tags=["Users"])


@router.post("/refresh")
async def refresh_token():
    pass


@router.post("/sing_up", response_model=TokenPair)
async def sing_up_user(
    data: SingUpUser,
    session: AsyncSession = Depends(get_session)
    ):
    user_id = await register_user(data=data, session=session)
    return TokenPair(access_token=sign_jwt(user_id),
                     refresh_token=sing_refresh_jwt(user_id))