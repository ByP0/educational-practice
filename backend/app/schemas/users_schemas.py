from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Annotated, Optional
from datetime import date
from email_validator import validate_email


class UserSchema(BaseModel):
    first_name: Annotated[str, Field(title="First name", examples=["Иван"])]
    last_name: Annotated[str, Field(title="Last name", examples=["Иванов"])]
    patronymic: Annotated[str, Field(title="Patronymic", examples=["Иванович"])]
    email: Annotated[str, Field(title="Email address", examples=["example@gmail.com"])]
    birth_date: Annotated[date, Field(title="Birth date", examples=["2025-04-22"])]


class ChangeUserSchema(BaseModel):
    first_name: Annotated[Optional[str] , Field(title="First name", examples=["Иван"], default=None)]
    last_name: Annotated[Optional[str], Field(title="Last name", examples=["Иванов"], default=None)]
    patronymic: Annotated[Optional[str], Field(title="Patronymic", examples=["Иванович"], default=None)]
    email: Annotated[Optional[str], Field(title="Email address", examples=["example@gmail.com"], default=None)]
    birth_date: Annotated[Optional[date], Field(title="Birth date", examples=["2025-04-22"], default=None)]

    @field_validator('email', mode='before')
    def check_email(cls, value):
        if value is not None:
            try:
                validated_email = validate_email(value)
                if validated_email is None:
                    raise ValueError(status_code=422, detail="Invalid email.")
            except:
                raise ValueError(status_code=422, detail="Invalid email.")

        return value
    

class NewPasswordSchema(BaseModel):
    old_password: Annotated[str, Field(title="Old user password", examples=["password"])]
    new_password: Annotated[str, Field(title="New user password", examples=["NewPassword"])]

    @model_validator(mode="before")
    def check_passwords(cls, values):
        old_password = values.get("old_password")
        new_password = values.get("new_password")
        if old_password == new_password:
            raise ValueError(status_code=422, detail="Passwords must not match.")
        
        return values