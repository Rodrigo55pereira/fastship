from typing import Any
from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from .schemas import ShipmentRead, ShipmentCreate, ShipmentStatus, ShipmentUpdate
from .database import shipments, save


app = FastAPI()


# shipments = {
#     # 12701: {
#     #     "weight": 2,
#     #     "content": "glassware",
#     #     # "status": "placed",
#     #     "destination": 11002,
#     # },
#     # 12702: {
#     #     "weight": 2.6,
#     #     "content": "books",
#     #     # "status": "shipped",
#     #     "destination": 11001,
#     # },
#     # 12701: {
#     #     "weight": 8,
#     #     "content": "glassware",
#     #     "status": "placed",
#     #     "destination": 11005,
#     # },
#     12702: {
#         "weight": 7.2,
#         "content": "books",
#         "status": "placed",
#         "destination": 11998,
#     },
#     12703: {
#         "weight": 15.0,
#         "content": "electronics",
#         "status": "in_transit",
#         "destination": 11500,
#     },
# }


@app.get("/shipment", response_model=ShipmentRead)  # shipment = remessa
def get_shipment(id: int):
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!!"
        )
    return shipments[id]


@app.post("/shipment")
def submit_shipment(shipment: ShipmentCreate) -> dict[str, Any]:

    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        **shipment.model_dump(),
        "id": new_id,
        "status": "placed",
    }
    save()
    return {"id": new_id}


@app.get("/shipment/{field}")
def get_shipement_field(field: str, id: int) -> Any:
    return shipments[id][field]


# @app.put("/shipment")
# def shipment_update(
#     id: int, content: str, weight: float, status: str
# ) -> dict[str, Any]:
#     shipments[id] = {
#         "content": content,
#         "weight": weight,
#         "status": status,
#     }
#     return shipments[id]


@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, body: ShipmentUpdate):

    shipments[id].update(body.model_dump(exclude_none=True))
    save()
    return shipments[id]


@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    shipments.pop(id)
    return {"detail": f"Shipment with id #{id} is deleted!"}


# Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
