from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import oauth2_scheme

from app.api.dependencies import SellerServiceDep
from app.api.schemas.seller import SellerCreate, SellerRead

router = APIRouter(
    prefix="/seller",
    tags=["Seller"],
)


### Register a seller
@router.post("/signup", response_model=SellerRead)
async def register_seller(
    seller: SellerCreate,
    service: SellerServiceDep,
):
    return await service.add(seller)


### Login the seller
@router.post("/login")
async def login_seller(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
):
    token = await service.token(
        request_form.username,
        request_form.password,
    )
    return {
        "access_token": token,
        "type": "jwt",
    }


@router.get("/dashboard")
async def get_dashboard(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    return {
        "token": token,
    }
