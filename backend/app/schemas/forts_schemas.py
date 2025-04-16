from pydantic import BaseModel, Field
from typing import Annotated


class FortsData(BaseModel):
    fort_id: Annotated[int, Field(title="Fort ID", examples=[5])]
    fort_name: Annotated[str, Field(title="Fort name", examples=["Король Фридрих Вильгельм III"])]
    description: Annotated[str, Field(title="Description", examples=["Военное фортификационное сооружение в Кёнигсберге (ныне Калининград), которое прикрывало шоссейную дорогу на Пиллау. Относится к кольцу фортов «Ночная перина Кёнигсберга»"])]
    images: Annotated[list[dict], Field(title="Images data", examples=[[{
        "image_id": 1,
        "filename": "photo_2025-04-15_11-13-51.jpg",
        "content_type": "image/jpeg",
        "image_data":"/9j/4AAQSkZJRgABAQAAAQABA"}
        ]])]


class FortAdd(BaseModel):
    fort_id: Annotated[int, Field(title="Fort ID", examples=[5])]
    fort_name: Annotated[str, Field(title="Fort name", examples=["Король Фридрих Вильгельм III"])]
    description: Annotated[str, Field(title="Description", examples=["Военное фортификационное сооружение в Кёнигсберге (ныне Калининград), которое прикрывало шоссейную дорогу на Пиллау. Относится к кольцу фортов «Ночная перина Кёнигсберга»"])]