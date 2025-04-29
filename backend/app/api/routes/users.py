from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from pydantic import Field

from app.schemas.users_schemas import UserSchema, ChangeUserSchema, NewPasswordSchema
from app.schemas.response_schemas import Response200
from app.database.postgres import get_session
from app.cruds.users_cruds import get_user_by_id, change_user_db, update_password, delete_user_db
from app.core.security import get_token_data, dependencies
from app.utils import validate_password


router = APIRouter(tags=["Users"], dependencies=dependencies)



@router.get("/me", response_model=UserSchema)
async def get_user(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    token_data = get_token_data(request=request)
    user = await get_user_by_id(user_id=token_data.get("user_id"), session=session)
    return user


@router.patch("/change", response_model=Response200)
async def change_user(
    request: Request,
    data: ChangeUserSchema,
    session: AsyncSession = Depends(get_session),
):
    token_data = get_token_data(request=request)
    await change_user_db(user_id=token_data.get("user_id"), data=data, session=session)
    return Response200


@router.post("/change-password", response_model=Response200)
async def change_user_password(
    request: Request,
    data: NewPasswordSchema,
    session: AsyncSession = Depends(get_session)
):
    token_data = get_token_data(request=request)
    user = await get_user_by_id(user_id=token_data.get("user_id"), session=session)
    validate_password(data.password, user.password.encode('utf-8'))
    await update_password(user_id=token_data.get("user_id"), new_password=data.new_password, session=session)
    return Response200


@router.delete("/delete", response_model=Response200)
async def delete_user(
    request: Request,
    password: Annotated[str, Field],
    session: AsyncSession = Depends(get_session)
):
    token_data = get_token_data(request=request)
    user = await get_user_by_id(user_id=token_data.get("user_id"), session=session)
    validate_password(password, user.password.encode('utf-8'))
    await delete_user_db(user_id=token_data.get("user_id"), session=session)
    return Response200