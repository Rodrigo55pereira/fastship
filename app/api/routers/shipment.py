from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Request, Form
from fastapi.templating import Jinja2Templates

from app.api.dependencies import ShipmentServiceDep, SellerDep, DeliveryPartnerDep
from app.api.schemas.shipment import ShipmentRead, ShipmentCreate, ShipmentUpdate
from app.config import app_settings
from app.utils import TEMPLATE_DIR

router = APIRouter(
    prefix="/shipment",
    tags=["Shipment"],
)

templates = Jinja2Templates(TEMPLATE_DIR)


@router.get("/", response_model=ShipmentRead)  # shipment = remessa
async def get_shipment(
    id: UUID,
    # _: SellerDep,  # O valor _ indica que nao será utilizado no metodo.
    service: ShipmentServiceDep,
):
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!!"
        )
    return shipment


### Tracking details of shipment
@router.get("/track")
async def get_tracking(
    request: Request,
    id: UUID,
    service: ShipmentServiceDep,
):
    shipment = await service.get(id)

    context = shipment.model_dump()
    context["status"] = shipment.status
    context["partner"] = shipment.delivery_partner.name
    context["timeline"] = shipment.timeline
    context["timeline"].reverse()

    return templates.TemplateResponse(
        request=request,
        name="track.html",
        context=context,
    )


@router.post("/")
async def submit_shipment(
    seller: SellerDep,
    shipment: ShipmentCreate,
    service: ShipmentServiceDep,
) -> ShipmentRead:
    return await service.add(shipment, seller)


@router.patch("/", response_model=ShipmentRead)
async def update_shipment(
    id: UUID,
    shipment_update: ShipmentUpdate,
    partner: DeliveryPartnerDep,
    service: ShipmentServiceDep,
):
    # converte em dicionario e tirar os nulos
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided to update"
        )

    return await service.update(
        id,
        shipment_update,
        partner,
    )


### Cancel s shipment by id
@router.get("/cancel", response_model=ShipmentRead)
async def cancel_shipment(
    id: UUID,
    seller: SellerDep,
    service: ShipmentServiceDep,
):
    return await service.cancel(id, seller)


### Sumbit a reivew for a shipment
@router.get("/review")
async def submit_review_page(
        request: Request,
        token: str,
):
    return templates.TemplateResponse(
        request=request,
        name="review.html",
        context={
            "review_url": f"http://{app_settings.APP_DOMAIN}/shipment/review?token={token}"
        }

    )


### Sumbit a reivew for a shipment
@router.post("/review")
async def submit_review(
        token: str,
        rating: Annotated[int, Form(ge=1, le=5)],
        comment: Annotated[str | None, Form()],
        service: ShipmentServiceDep,
):
    await service.rate(token, rating, comment)
    return {"detail": "Review submitted"}