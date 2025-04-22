from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, func
from fastapi import HTTPException
import base64
from datetime import datetime

from app.models.models import Tours, UserTours, Image, Forts
from app.schemas.tours_schemas import ToursData, TourAdd, TourPatch


async def get_tours_by_fort_id(fort_id: int, session: AsyncSession) -> list[ToursData]:
    current_time = datetime.now()
    
    stmt = select(Tours).where(Tours.fort_id==fort_id).where(Tours.tour_date >= current_time)
    result: Result = await session.execute(stmt)
    tours = result.scalars().all()
    if not tours:
        raise HTTPException(status_code=404, detail="Tours not found")
    
    return [ToursData(
        tour_id=tour.tour_id,
        gathering_place=tour.gathering_place,
        tour_date=tour.tour_date,
        number_of_seats=tour.number_of_seats,
        fort_id=tour.fort_id
        )
        for tour in tours]

async def get_user_tours(user_id: int, session: AsyncSession) -> list[ToursData]:
    current_time = datetime.now()

    stmt = (
        select(Tours)
        .join(Image, Tours.fort_id == Image.fort_id, isouter=True)
        .where(Tours.user_id == user_id)
        .where(Tours.tour_date >= current_time)
        .order_by(Tours.tour_id)
    )   
    result: Result = await session.execute(stmt)
    tours = result.scalars().all()    
    if not tours:
        raise HTTPException(status_code=404, detail="Tours not found")
    
    tours_data = []   
    for tour in tours:
        fort_stmt = (
            select(Forts.fort_name)
            .where(Forts.fort_id == tour.fort_id)
        )        
        fort_result: Result = await session.execute(fort_stmt)
        fort_name = fort_result.scalar_one_or_none()
        last_image_stmt = (
            select(Image)
            .where(Image.fort_id == tour.fort_id)
            .order_by(Image.created_at.desc())
            .limit(1)
        )
        
        last_image_result: Result = await session.execute(last_image_stmt)
        last_image = last_image_result.scalars().first()
        image_data = None
        if last_image:
            encoded_image_data = base64.b64encode(last_image.image_data).decode('utf-8')
            image_data = {
                "image_id": last_image.image_id,
                "filename": last_image.filename,
                "content_type": last_image.content_type,
                "image_data": encoded_image_data
            }

        tours_data.append(ToursData(
            tour_id=tour.tour_id,
            gathering_place=tour.gathering_place,
            tour_date=tour.tour_date,
            number_of_seats=tour.number_of_seats,
            fort_id=tour.fort_id,
            fort_name=fort_name if fort_name else "",
            image=image_data
        ))
    return tours_data


async def delete_tour_db(tour_id: int, session: AsyncSession):
    stmt = select(Tours).where(Tours.tour_id == tour_id)
    result: Result = await session.execute(stmt)
    tour = result.scalar_one_or_none()

    if tour is None:
        raise HTTPException(status_code=404, detail="Tour not found")

    await session.delete(tour)
    await session.commit()

async def add_tour_db(data: TourAdd, session: AsyncSession, user_id: int):
    data_for_db = Tours(
        gathering_place=data.gathering_place,
        tour_date=data.tour_date,
        number_of_seats=data.number_of_seats,
        fort_id=data.fort_id,
        user_id=user_id,
    )
    session.add(data_for_db)
    await session.commit()
    await session.refresh(data_for_db)
    
async def patch_tour_tb(tour_id: int, data: TourPatch, session: AsyncSession):
    stmt = select(Tours).where(Tours.tour_id == tour_id)
    
    result: Result = await session.execute(stmt)
    tour = result.scalar_one_or_none()
    
    if tour is None:
        raise HTTPException(status_code=404, detail=f"Tour with id {tour_id} not found.")

    if data.fort_id is not None:
        tour.fort_id = data.fort_id
    if data.gathering_place is not None:
        tour.gathering_place = data.gathering_place
    if data.tour_date is not None:
        tour.tour_date = data.tour_date
    if data.number_of_seats is not None:
        tour.number_of_seats = data.number_of_seats
    
    await session.commit()

async def register_user_to_tour(user_id: int, tour_id: int, session: AsyncSession):
    try:
        stmt_tour = select(Tours.number_of_seats).where(Tours.tour_id == tour_id)
        result_tour = await session.execute(stmt_tour)
        available_seats = result_tour.scalar_one_or_none()
        
        if available_seats is None:
            raise HTTPException(status_code=404, detail="Tour not found")

        stmt_count = select(func.count(UserTours.id)).where(UserTours.tour_id == tour_id)    
        result_count = await session.execute(stmt_count)
        registered_count = result_count.scalar()

        if registered_count >= available_seats:
            raise HTTPException(status_code=400, detail="No available seats")
             
        data_for_db = UserTours(user_id=user_id, tour_id=tour_id)
        session.add(data_for_db)
        await session.commit()
        await session.refresh(data_for_db)
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
