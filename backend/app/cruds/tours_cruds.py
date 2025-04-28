from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, func
from fastapi import HTTPException
import base64
from datetime import datetime

from app.models.models import Tours, Image, Forts
from app.schemas.tours_schemas import ToursData, TourAdd, TourPatch


async def get_tours_by_fort_id(fort_id: int, session: AsyncSession) -> list[ToursData]:
    try:
        current_time = datetime.now()

        stmt = (
            select(
                Tours,
                Forts.fort_name,
                Image.image_id,
                Image.filename,
                Image.content_type,
                Image.image_data
            )
            .join(Forts, Tours.fort_id == Forts.fort_id)
            .outerjoin(Image, Tours.fort_id == Image.fort_id)
            .where(Tours.tour_date >= current_time)
            .order_by(Tours.tour_id)
        )

        result: Result = await session.execute(stmt)
        tours = result.all()

        if not tours:
            raise HTTPException(status_code=404, detail="Tours not found")

        tours_data = []
        for tour, fort_name, image_id, filename, content_type, image_data in tours:
            encoded_image_data = None
            if image_data:
                encoded_image_data = base64.b64encode(image_data).decode('utf-8')

            tours_data.append(ToursData(
                tour_id=tour.tour_id,
                gathering_place=tour.gathering_place,
                tour_date=tour.tour_date,
                number_of_seats=tour.number_of_seats,
                cost=tour.cost,
                fort_id=tour.fort_id,
                fort_name=fort_name if fort_name else "",
                image={
                    "image_id": image_id,
                    "filename": filename,
                    "content_type": content_type,
                    "image_data": encoded_image_data
                } if image_data else None
            ))

        unique_tours = {tour.tour_id: tour for tour in tours_data}

        return list(unique_tours.values())
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_user_tours(user_id: int, session: AsyncSession) -> list[ToursData]:
    try:
        current_time = datetime.now()

        stmt = (
            select(
                Tours,
                Forts.fort_name,
                Image.image_id,
                Image.filename,
                Image.content_type,
                Image.image_data
            )
            .join(Forts, Tours.fort_id == Forts.fort_id)
            .outerjoin(Image, Tours.fort_id == Image.fort_id)
            .where(Tours.user_id == user_id)
            .where(Tours.tour_date >= current_time)
            .order_by(Tours.tour_id)
        )

        result: Result = await session.execute(stmt)
        tours = result.all()

        if not tours:
            raise HTTPException(status_code=404, detail="Tours not found")

        tours_data = []
        for tour, fort_name, image_id, filename, content_type, image_data in tours:
            encoded_image_data = None
            if image_data:
                encoded_image_data = base64.b64encode(image_data).decode('utf-8')

            tours_data.append(ToursData(
                tour_id=tour.tour_id,
                gathering_place=tour.gathering_place,
                tour_date=tour.tour_date,
                number_of_seats=tour.number_of_seats,
                cost=tour.cost,
                fort_id=tour.fort_id,
                fort_name=fort_name if fort_name else "",
                image={
                    "image_id": image_id,
                    "filename": filename,
                    "content_type": content_type,
                    "image_data": encoded_image_data
                } if image_data else None
            ))

        unique_tours = {tour.tour_id: tour for tour in tours_data}

        return list(unique_tours.values())
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def delete_tour_db(tour_id: int, session: AsyncSession):
    try:
        stmt = select(Tours).where(Tours.tour_id == tour_id)
        result: Result = await session.execute(stmt)
        tour = result.scalar_one_or_none()

        if tour is None:
            raise HTTPException(status_code=404, detail="Tour not found")

        await session.delete(tour)
        await session.commit()

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def add_tour_db(data: TourAdd, session: AsyncSession, user_id: int):
    try:
        data_for_db = Tours(
            gathering_place=data.gathering_place,
            tour_date=data.tour_date,
            number_of_seats=data.number_of_seats,
            cost=data.cost,
            fort_id=data.fort_id,
            user_id=user_id,
        )
        session.add(data_for_db)
        await session.commit()
        await session.refresh(data_for_db)
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def patch_tour_tb(tour_id: int, data: TourPatch, session: AsyncSession):
    try:
        stmt = select(Tours).where(Tours.tour_id == tour_id)
        
        result: Result = await session.execute(stmt)
        tour = result.scalar_one_or_none()
        
        if tour is None:
            raise HTTPException(status_code=404, detail=f"Tour with id {tour_id} not found.")

        if data.gathering_place is not None:
            tour.gathering_place = data.gathering_place
        if data.tour_date is not None:
            tour.tour_date = data.tour_date
        if data.number_of_seats is not None:
            tour.number_of_seats = data.number_of_seats
        if data.cost is not None:
            tour.cost = data.cost
        
        await session.commit()

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))