from pydantic import BaseModel, Field, field_validator
from typing import Annotated
from email_validator import validate_email

from backend.config import example_jwt_token


class SingUpUser(BaseModel):
    first_name: Annotated[str, Field(title="First name", examples=["Иван"])]
    last_name: Annotated[str, Field(title="Last name", examples=["Иванов"])]
    patronymic: Annotated[str, Field(title="Patronymic", examples=["Иванович"])]
    email: Annotated[str, Field(title="Email address", examples=["example@gmail.com"])]
    password: Annotated[str, Field(title="Password", examples=["password"])]
    birth_date: Annotated[str, Field(title="Birth date", examples=["Ну что-то хз пока"])]

    @field_validator('email', mode='before')
    def check_email(cls, value):
        if value is not None:
            try:
                validated_email = validate_email(value)
                if validated_email is None:
                    raise ValueError("Invalid email.")
            except:
                raise ValueError("Invalid email.")

        return value

class TokenPair(BaseModel):
    access_token: Annotated[str, Field(title="Access jwt token", examples=[example_jwt_token])]
    refresh_token: Annotated[str, Field(title="Refresh jwt token", examples=[example_jwt_token])]

class SingInUser(BaseModel):
    email: Annotated[str, Field(title="Email address", examples=["example@gmail.com"])]
    password: Annotated[str, Field(title="Password", examples=["password"])]

    @field_validator('email', mode='before')
    def check_email(cls, value):
        if value is not None:
            try:
                validated_email = validate_email(value)
                if validated_email is None:
                    raise ValueError("Invalid email.")
            except:
                raise ValueError("Invalid email.")

        return value