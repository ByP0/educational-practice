from pydantic import BaseModel, Field
from typing import Annotated, Optional
from datetime import datetime


class ToursData(BaseModel):
    tour_id: Annotated[int, Field(title="Tour ID", examples=[1])]
    gathering_place: Annotated[str, Field(title="Tour gathering place", examples=["ул. M.A. Булатова, Форт №5"])]
    tour_date: Annotated[datetime, Field(title="Tour date", examples=["2024-12-07 03:21:37.273427"])]
    number_of_seats: Annotated[int, Field(title="Number of seats", examples=[20])]
    cost: Annotated[Optional[int], Field(title="Cost tour", examples=[200], default=200)]
    fort_id: Annotated[int, Field(title="Fort ID", examples=[5])]
    fort_name: Annotated[str, Field(title="Fort name", examples=["Король Фридрих Вильгельм III"])]
    image: Annotated[dict, Field(title="Images data", examples=[{
        "image_id": 1,
        "filename": "photo_2025-04-15_11-13-51.jpg",
        "content_type": "image/jpeg",
        "image_data":"/9j/4AAQSkZJRgABAQAAAQABA"}
        ])]
    

class TourAdd(BaseModel):
    gathering_place: Annotated[str, Field(title="Tour gathering place", examples=["ул. M.A. Булатова, Форт №5"])]
    tour_date: Annotated[datetime, Field(title="Tour date", examples=["2024-12-07 03:21:37.273427"])]
    number_of_seats: Annotated[int, Field(title="Number of seats", examples=[20])]
    cost: Annotated[Optional[int], Field(title="Cost tour", examples=[200], default=200)]
    fort_id: Annotated[int, Field(title="Fort ID", examples=[5])]


class TourPatch(BaseModel):
    gathering_place: Annotated[Optional[str], Field(title="Tour gathering place", examples=["ул. M.A. Булатова, Форт №5"], default=None)]
    tour_date: Annotated[Optional[datetime], Field(title="Tour date", examples=["2024-12-07 03:21:37.273427"], default=None)]
    number_of_seats: Annotated[Optional[int], Field(title="Number of seats", examples=[20], default=None)]
    cost: Annotated[Optional[int], Field(title="Cost tour", examples=[200], default=200)]