from pydantic import BaseModel, Field
from typing import Annotated


class Response200(BaseModel):
    status_code: Annotated[int, Field(title="Status code", default=200, examples=[200])]
    detail: Annotated[str, Field(title="Rresponse detail", default="OK", examples=["OK"])]
    