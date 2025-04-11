from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime


class ToursData(BaseModel):
    tour_id: Annotated[int, Field(title="Tour ID", examples=[1])]
    gathering_place: Annotated[str, Field(title="Tour gathering place", examples=["ул. M.A. Булатова, Форт №5"])]
    tour_date: Annotated[datetime, Field(title="Tour date", examples=["2024-12-07 03:21:37.273427"])]
    number_of_seats: Annotated[int, Field(title="Number of seats", examples=[20])]
    fort_id: Annotated[int, Field(title="Fort ID", examples=[5])]


class TourAdd(BaseModel):
    gathering_place: Annotated[str, Field(title="Tour gathering place", examples=["ул. M.A. Булатова, Форт №5"])]
    tour_date: Annotated[datetime, Field(title="Tour date", examples=["2024-12-07 03:21:37.273427"])]
    number_of_seats: Annotated[int, Field(title="Number of seats", examples=[20])]
    fort_id: Annotated[int, Field(title="Fort ID", examples=[5])]