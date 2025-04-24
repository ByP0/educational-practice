from sqlalchemy import BigInteger, ForeignKey, Text, Integer, LargeBinary, Date, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date


Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(Text)
    last_name: Mapped[str] = mapped_column(Text)
    patronymic: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text, unique=True)
    password: Mapped[str] = mapped_column(Text)
    birth_date: Mapped[date] = mapped_column(Date)


class Forts(Base):
    __tablename__ = "forts"

    fort_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fort_name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)


class Image(Base):
    __tablename__ = "images"

    image_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(Text)
    content_type: Mapped[str] = mapped_column(Text)
    image_data: Mapped[bytes] = mapped_column(LargeBinary)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    fort_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("forts.fort_id"))


class Tours(Base):
    __tablename__ = "tours"

    tour_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    gathering_place: Mapped[str] = mapped_column(Text)
    tour_date: Mapped[datetime] = mapped_column()
    number_of_seats: Mapped[int] = mapped_column(Integer)
    cost: Mapped[int] = mapped_column(Integer, default=200)
    fort_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("forts.fort_id"))
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))


class Sessions(Base):
    __tablename__ = "sessions"

    session: Mapped[str] = mapped_column(Text, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))


class UserTours(Base):
    __tablename__ = "user_tours"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))
    tour_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("tours.tour_id"))