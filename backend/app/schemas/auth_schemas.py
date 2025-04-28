from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException
from typing import Annotated
from datetime import date
from email_validator import validate_email

from app.config import example_jwt_token


class RegisterUser(BaseModel):
    first_name: Annotated[str, Field(title="First name", examples=["Иван"])]
    last_name: Annotated[str, Field(title="Last name", examples=["Иванов"])]
    patronymic: Annotated[str, Field(title="Patronymic", examples=["Иванович"])]
    email: Annotated[str, Field(title="Email address", examples=["example@gmail.com"])]
    password: Annotated[str, Field(title="Password", examples=["password"])]
    birth_date: Annotated[date, Field(title="Birth date", examples=["2025-04-22"])]

    @field_validator('email', mode='before')
    def check_email(cls, value):
        if value is not None:
            try:
                validated_email = validate_email(value)
                if validated_email is None:
                    raise HTTPException(status_code=422, detail="Invalid email.")
            except:
                raise HTTPException(status_code=422, detail="Invalid email.")

        return value
    

class LoginUser(BaseModel):
    email: Annotated[str, Field(title="Email address", examples=["example@gmail.com"])]
    password: Annotated[str, Field(title="Password", examples=["password"])]

    @field_validator('email', mode='before')
    def check_email(cls, value):
        if value is not None:
            try:
                validated_email = validate_email(value)
                if validated_email is None:
                    raise HTTPException(status_code=422, detail="Invalid email.")
            except:
                raise HTTPException(status_code=422, detail="Invalid email.")

        return value


class TokenPair(BaseModel):
    access_token: Annotated[str, Field(title="Access JWT-token", examples=[example_jwt_token])]
    refresh_token: Annotated[str, Field(title="Refresh JWT-token", examples=[example_jwt_token])]