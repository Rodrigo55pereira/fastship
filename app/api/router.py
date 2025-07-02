from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import ServiceDep
from app.api.schemas.shipment import ShipmentCreate, ShipmentUpdate
from app.database.models import Shipment

router = APIRouter()


@router.get("/shipment", response_model=Shipment)  # shipment = remessa
async def get_shipment(id: int, service: ServiceDep):
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!!"
        )
    return shipment


@router.post("/shipment")
async def submit_shipment(shipment: ShipmentCreate, service: ServiceDep) -> Shipment:
    return await service.add(shipment)


@router.patch("/shipment", response_model=Shipment)
async def update_shipment(id: int, shipment_update: ShipmentUpdate, service: ServiceDep):
    # converte em dicionario e tirar os nulos
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided to update"
        )

    shipment = await service.update(id, update)
    return shipment


@router.delete("/shipment")
async def delete_shipment(id: int, service: ServiceDep) -> dict[str, str]:
    await service.delete(id)
    return {"detail": f"Shipment with id #{id} is deleted!"}
