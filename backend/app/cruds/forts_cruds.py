from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, desc
from fastapi import HTTPException
import base64


from app.models.models import Forts, Image
from app.schemas.forts_schemas import FortAdd, FortsData


async def get_forts(session: AsyncSession) -> list[FortsData]:
    try:
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
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_one_fort(fort_id: int, session: AsyncSession) -> FortsData:
    try:
        stmt_forts = select(Forts).where(Forts.fort_id == fort_id)
        result_forts: Result = await session.execute(stmt_forts)
        fort = result_forts.scalar_one_or_none()
        if fort is None:
            raise HTTPException(status_code=404, detail="Fort not found")
        stmt_images = (
            select(Image)
            .where(Image.fort_id == fort_id)
            .order_by(desc(Image.created_at))
            .limit(1)
        )
        result_images: Result = await session.execute(stmt_images)
        image = result_images.scalar_one_or_none()

        image_data = None
        if image is not None:
            image_data = {
                "image_id": image.image_id,
                "filename": image.filename,
                "content_type": image.content_type,
                "image_data": base64.b64encode(image.image_data).decode('utf-8')
            }       

        return FortsData(
            fort_id=fort.fort_id,
            fort_name=fort.fort_name,
            description=fort.description,
            images=[image_data] if image_data else []
        )
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def add_fort_db(data: FortAdd, session: AsyncSession):
    try:
        data_for_db = Forts(
            fort_id=data.fort_id,
            fort_name=data.fort_name,
            description=data.description,
        )
        session.add(data_for_db)
        await session.commit()
        await session.refresh(data_for_db)

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def add_image_fort(fort_id: int, image, session: AsyncSession):
    try:
        image_data = await image.read()
        data_for_db = Image(
            filename=image.filename,
            content_type=image.content_type,
            image_data=image_data,
            fort_id=fort_id
        )
        session.add(data_for_db)

        await session.commit()
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))