from datetime import datetime
from enum import Enum

from uuid import uuid4, UUID

from pydantic import EmailStr
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlmodel import Field, SQLModel, Relationship


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"
    """
        Você está especificando que, no banco de dados (PostgreSQL),
        essa coluna deve ser do tipo UUID.
    """
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        ),
    )
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime

    seller_id: UUID = Field(foreign_key="seller.id")
    """
        Cria uma propriedade automática chamada seller, 
        que ao acessar um objeto Shipment, 
        te permite acessar o vendedor desse shipment.
    """
    seller: "Seller" = Relationship(
        # O parâmetro back_populates serve para ligar as duas pontas do relacionamento.
        back_populates="shipments",
        # significa que, quando você buscar um seller, ele já busca junto todos os
        # shipments relacionados (faz um SELECT extra automaticamente).
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class Seller(SQLModel, table=True):

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        ),
    )

    name: str

    email: EmailStr
    password_hash: str

    shipments: list[Shipment] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
