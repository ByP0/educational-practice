from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
import base64
from fastapi import HTTPException

from app.models.models import Forts, Image
from app.schemas.forts_schemas import FortAdd, FortsData


async def get_forts(session: AsyncSession) -> list[FortsData]:
    stmt_forts = select(Forts)
    result_forts: Result = await session.execute(stmt_forts)
    forts = result_forts.scalars().all()

    forts_ids = [fort.fort_id for fort in forts]
    stmt_images = select(Image).where(Image.fort_id.in_(forts_ids))
    result_images: Result = await session.execute(stmt_images)
    images = result_images.scalars().all()

    images_dict = {}
    for image in images:
        if image.fort_id not in images_dict:
            images_dict[image.fort_id] = []
        encoded_image_data = base64.b64encode(image.image_data).decode('utf-8')
        images_dict[image.fort_id].append({
            "image_id": image.image_id,
            "filename": image.filename,
            "content_type": image.content_type,
            "image_data": encoded_image_data,
        })

    return [FortsData(
        fort_id=fort.fort_id,
        fort_name=fort.fort_name,
        description=fort.description,
        images=images_dict.get(fort.fort_id, [])
        ) for fort in forts]

async def get_one_fort(fort_id: int, session: AsyncSession) -> FortsData:
    stmt_forts = select(Forts).where(Forts.fort_id == fort_id)
    result_forts: Result = await session.execute(stmt_forts)
    fort = result_forts.scalar_one_or_none()

    if fort is None:
        raise HTTPException(status_code=404, detail="Fort not found")

    stmt_images = select(Image).where(Image.fort_id == fort_id)
    result_images: Result = await session.execute(stmt_images)
    images = result_images.scalars().all()

    image_data = [
        {
            "image_id": image.image_id,
            "filename": image.filename,
            "content_type": image.content_type,
            "image_data": base64.b64encode(image.image_data.encode('utf-8')).decode('utf-8') if isinstance(image.image_data, str) else base64.b64encode(image.image_data).decode('utf-8'),
        }
        for image in images
    ]

    return FortsData(
        fort_id=fort.fort_id,
        fort_name=fort.fort_name,
        description=fort.description,
        images=image_data,
    )

async def add_fort_db(data: FortAdd, session: AsyncSession):
    data_for_db = Forts(
        fort_id=data.fort_id,
        fort_name=data.fort_name,
        description=data.description,
    )
    session.add(data_for_db)
    await session.commit()
    await session.refresh(data_for_db)

async def add_image_fort(fort_id: int, image, session: AsyncSession):
    image_data = await image.read()
    data_for_db = Image(
        filename=image.filename,
        content_type=image.content_type,
        image_data=image_data,
        fort_id=fort_id
    )
    session.add(data_for_db)

    await session.commit()