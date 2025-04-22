from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from fastapi import HTTPException
import os

from app.config import db_url
from app.models.models import Base, Forts, Image
from app.database.data_forts.data_forts import forts_id_list, forts_name_list, forts_descriptions


engine = create_async_engine(
    url=str(db_url),
    echo=True,
    future=True,
    )

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

async def get_session():
    async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
    async with async_session() as session:
        yield session
        await session.close()

async def upload_forts(session: AsyncSession, image_folder_path: str):
    try:
        for i in range(len(forts_id_list)):
            data_for_db = Forts(
                fort_id=forts_id_list[i],
                fort_name=forts_name_list[i],
                description=forts_descriptions[i]
            )
            session.add(data_for_db)
            await session.commit()
            await session.refresh(data_for_db)

            image_filename = f"{forts_id_list[i]}.png"
            image_path = os.path.join(image_folder_path, image_filename)

            if os.path.isfile(image_path):
                with open(image_path, 'rb') as image_file:
                    image_data = image_file.read()

                image_for_db = Image(
                    filename=image_filename,
                    content_type='image/png',
                    image_data=image_data,
                    fort_id=data_for_db.fort_id
                )

                session.add(image_for_db)
            else:
                print(f"Warning: Image file {image_filename} does not exist, skipping.")
            
        await session.commit()
        
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))