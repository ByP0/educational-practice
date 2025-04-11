from pydantic import BaseModel, Field
from typing import Annotated


class FortsData(BaseModel):
    pass


class FortAdd(BaseModel):
    fort_id: Annotated[int, Field(title="Fort ID", examples=[5])]
    fort_name: Annotated[str, Field(title="Fort name", examples=["Король Фридрих Вильгельм III"])]
    description: Annotated[str, Field(title="Description", examples=["военное фортификационное сооружение в Кёнигсберге (ныне Калининград), которое прикрывало шоссейную дорогу на Пиллау. Относится к кольцу фортов «Ночная перина Кёнигсберга»"])]