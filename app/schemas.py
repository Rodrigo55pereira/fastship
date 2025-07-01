from datetime import datetime
from random import randint
from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from app.database.models import ShipmentStatus


def random_destination():
    return randint(11000, 11999)


class BaseShipment(SQLModel):
    content: str
    weight: float = Field(le=25)
    destination: int


class Shipment(BaseShipment, table=True):
    id: int = Field(default=None, primary_key=True)
    status: ShipmentStatus
    estimated_delivery: datetime


class ShipmentCreate(BaseShipment):
    pass


class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)
