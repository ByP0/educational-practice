from pydantic import BaseModel, Field, model_validator
from typing import Annotated, Optional
from datetime import datetime, timezone


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

    @model_validator(mode="before")
    def check_model(cls, values):
        tour_date = values.get("tour_date")
        try:
            cleaned_tour_date = tour_date.split(" (")[0].replace("GMT", "")
            parsed_date = datetime.strptime(cleaned_tour_date, '%a %b %d %Y %H:%M:%S %z')
            time_part = tour_date.split(" (")[1].strip() if "(" in tour_date else "00:00"
            hours, minutes = map(int, time_part.split(":")[:2])
            parsed_date = parsed_date.replace(hour=hours, minute=minutes)
            values["tour_date"] = parsed_date.replace(tzinfo=None)

        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")

        return values
    
class TourPatch(BaseModel):
    gathering_place: Annotated[Optional[str], Field(title="Tour gathering place", examples=["ул. M.A. Булатова, Форт №5"], default=None)]
    tour_date: Annotated[Optional[datetime], Field(title="Tour date", examples=["2024-12-07 03:21:37.273427"], default=None)]
    number_of_seats: Annotated[Optional[int], Field(title="Number of seats", examples=[20], default=None)]
    fort_id: Annotated[Optional[int], Field(title="Fort ID", examples=[5], default=None)]

    @model_validator(mode="before")
    def check_model(cls, values):
        tour_date = values.get("tour_date")
        if tour_date:
            values["tour_date"] = datetime.strptime(tour_date.split(" (")[0].replace("GMT", "+")[:25] + tour_date.split("GMT")[1][:5],'%a %b %d %Y %H:%M:%S %z').astimezone(datetime.timezone.utc)
        
        return values
