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
    

class UserSession(BaseModel):
    session: Annotated[str, Field(title="User session", examples=["123e4567-e89b-12d3-a456-426614174000"])]