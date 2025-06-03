from typing import Any
from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()


shipments = {
    12701: {
        "weight": 0.6,
        "content": "glassware",
        "status": "placed",
    },
    12702: {
        "weight": 2.6,
        "content": "books",
        "status": "shipped",
    },
}


@app.get("/shipment")  # shipment = remessa
def get_shipment(id: int) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!!"
        )
    return shipments[id]


@app.post("/shipment")
def submit_shipment(weight: float, data: dict[str, str]) -> dict[str, Any]:

    content = data["content"]

    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Maximum weight limit is 25 kgs",
        )

    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        "content": content,
        "weight": weight,
        "status": "placed",
    }

    return {"id": new_id}


@app.get("/shipment/{field}")
def get_shipement_field(field: str, id: int) -> Any:
    return shipments[id][field]


@app.put("/shipment")
def shipment_update(
    id: int, content: str, weight: float, status: str
) -> dict[str, Any]:
    shipments[id] = {
        "content": content,
        "weight": weight,
        "status": status,
    }
    return shipments[id]


# Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
