from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.services.shipment import ShipmentService
from app.services.seller import SellerService
from app.core.security import oauth2_scheme
from app.database.models import Seller
from app.utils import decode_access_token
from redis_conn import is_jti_blacklisted

# Session Dependency Annotation
SessionDep = Annotated[AsyncSession, Depends(get_session)]


# Access token data dep
async def get_access_token(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> dict:
    data = decode_access_token(token)

    if data is None or await is_jti_blacklisted(data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
        )

    return data


# Logged In Seller
async def get_current_seller(
    token_data: Annotated[dict, Depends(get_access_token)],
    session: SessionDep,
):
    return await session.get(Seller, token_data["user"]["id"])


def get_shipment_service(session: SessionDep):
    return ShipmentService(session)


def get_seller_service(session: SessionDep):
    return SellerService(session)


ShipmentServiceDep = Annotated[
    ShipmentService,
    Depends(get_shipment_service),
]

SellerServiceDep = Annotated[
    SellerService,
    Depends(get_seller_service),
]

SellerDep = Annotated[
    Seller,
    Depends(get_current_seller),
]
