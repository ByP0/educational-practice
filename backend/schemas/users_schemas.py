from pydantic import BaseModel, Field


class SingUpUser(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    email: str
    password: str
    birth_date: str

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str

class SingInUser(BaseModel):
    email: str
    password: str