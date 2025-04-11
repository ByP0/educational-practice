from sqlalchemy import BigInteger, VARCHAR, TIME, ForeignKey, DATE, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date


Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(Text)
    last_name: Mapped[str] = mapped_column(Text)
    patronymic: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text, unique=True)
    password: Mapped[str] = mapped_column(Text)
    birth_date: Mapped[str] = mapped_column(Text)


class Forts(Base):
    __tablename__ = "forts"

    fort_id: Mapped[int] = mapped_column(BigInteger)
    fort_name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)


class Image(Base):
    __tablename__ = "images"

    image_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(Text)
    content_type: Mapped[str] = mapped_column(Text)
    image_data: Mapped[str] = mapped_column(Text)
    fort_id : Mapped[str] = mapped_column(BigInteger, ForeignKey("forts.fort_id"))
    