from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from fastapi import HTTPException
import base64

from app.models.models import Tickets, Tours, Forts, Image
from app.schemas.tickets_schemas import TicketsDataSchema


async def create_ticket(user_id: int, tour_id: int, session: AsyncSession):
    stmt = select(Tours).where(Tours.tour_id == tour_id)
    result: Result = await session.execute(stmt)
    tour = result.scalar_one_or_none()
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found.")
    new_ticket = Tickets(user_id=user_id, tour_id=tour_id)
    session.add(new_ticket)
    await session.commit()

async def get_user_tickets(user_id: int, session: AsyncSession) -> list[TicketsDataSchema]:
    stmt = (
        select(
            Tickets,
            Tours.tour_id,
            Tours.gathering_place,
            Tours.tour_date,
            Tours.number_of_seats,
            Tours.cost,
            Tours.fort_id,
            Forts.fort_name,
            Image.image_id,
            Image.filename,
            Image.content_type,
            Image.image_data
        )
        .join(Tours, Tickets.tour_id == Tours.tour_id)
        .join(Forts, Tours.fort_id == Forts.fort_id)
        .outerjoin(Image, Tours.fort_id == Image.fort_id)
        .where(Tickets.user_id == user_id)
    )

    result: Result = await session.execute(stmt)
    tickets = result.all()

    if not tickets:
        raise HTTPException(status_code=404, detail="No tickets found for this user.")

    tickets_data = {}
    for ticket, tour_id, gathering_place, tour_date, number_of_seats, cost, fort_id, fort_name, image_id, filename, content_type, image_data in tickets:
        encoded_image_data = None
        if image_data:
            encoded_image_data = base64.b64encode(image_data).decode('utf-8')

        ticket_data = TicketsDataSchema(
            ticket_id=ticket.id,
            tour_id=tour_id,
            gathering_place=gathering_place,
            tour_date=tour_date,
            number_of_seats=number_of_seats,
            cost=cost,
            fort_id=fort_id,
            fort_name=fort_name if fort_name else "",
            image={
                "image_id": image_id,
                "filename": filename,
                "content_type": content_type,
                "image_data": encoded_image_data
            } if image_data else None
        )

        if ticket.id not in tickets_data:
            tickets_data[ticket.id] = ticket_data

    return list(tickets_data.values())