from datetime import datetime, timedelta
from typing import Any
from fastapi import APIRouter, HTTPException, status

from app.database.models import ShipmentStatus
from app.database.session import SessionDep
from app.schemas import Shipment, ShipmentCreate, ShipmentUpdate

router = APIRouter()

@router.get("/shipment", response_model=Shipment)  # shipment = remessa
async def get_shipment(id: int, session: SessionDep):

    shipment = await session.get(Shipment, id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!!"
        )
    return shipment


@router.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate, session: SessionDep) -> dict[str, Any]:
    new_shipment = Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=3),
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)

    return {"id": new_shipment.id}


@router.patch("/shipment", response_model=Shipment)
def update_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDep):
    # converte em dicionario e tirar os nulos
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided to update"
        )

    shipment = session.get(Shipment, id)
    shipment.sqlmodel_update(update)  # type:ignore

    session.add(shipment)
    session.commit()
    session.refresh(shipment)

    return shipment


@router.delete("/shipment")
def delete_shipment(id: int, session: SessionDep) -> dict[str, str]:

    session.delete(session.get(Shipment, id))

    session.commit()

    return {"detail": f"Shipment with id #{id} is deleted!"}


