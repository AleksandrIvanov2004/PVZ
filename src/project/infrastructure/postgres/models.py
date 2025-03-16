from sqlalchemy import Enum
import enum
from datetime import datetime
from tkinter.constants import CASCADE

from sqlalchemy.orm import Mapped, mapped_column
from project.infrastructure.postgres.database import Base
from sqlalchemy import ForeignKey

class StatusEnum_(str, enum.Enum):
    NOT_SENT = "NOT_SENT",
    DELIVERED_IN_PVZ = "DELIVERED_IN_PVZ"
    RECEIVED = "RECEIVED"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    region: Mapped[int] = mapped_column(nullable=False)


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(nullable=False, unique=True)
    region: Mapped[int] = mapped_column(nullable=False)


class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id", ondelete=CASCADE,
                                                       onupdate=CASCADE), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete=CASCADE,
                                                    onupdate=CASCADE), nullable=False)


class PickUpPoint(Base):
    __tablename__ = "pick_up_points"

    id: Mapped[int] = mapped_column(primary_key=True)
    region: Mapped[int] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)


class Worker(Base):
    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete=CASCADE,
                                                    onupdate=CASCADE), nullable=False)
    pick_up_point_id: Mapped[int] = mapped_column(ForeignKey("pick_up_points.id", ondelete=CASCADE,
                                                             onupdate=CASCADE), nullable=False)


class WorkingShift(Base):
    __tablename__ = "working_shifts"

    id: Mapped[int] = mapped_column(primary_key=True)
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete=CASCADE,
                                                    onupdate=CASCADE), nullable=False)
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column(nullable=False)


class Supply(Base):
    __tablename__ = "supplies"

    id: Mapped[int] = mapped_column(primary_key=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id", ondelete=CASCADE,
                                                      onupdate=CASCADE), nullable=False)
    pick_up_point_id: Mapped[int] = mapped_column(ForeignKey("pick_up_points.id", onupdate=CASCADE,
                                                             ondelete=CASCADE), nullable=False)
    time: Mapped[datetime] = mapped_column(nullable=False)


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    supply_id: Mapped[int] = mapped_column(ForeignKey("supplies.id", ondelete=CASCADE,
                                                       onupdate=CASCADE), nullable=False)
    status: Mapped[StatusEnum_] = mapped_column(nullable=False)

