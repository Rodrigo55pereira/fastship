from typing import Annotated

from fastapi import APIRouter, Depends, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from starlette.templating import Jinja2Templates

from app.api.dependencies import SellerServiceDep, get_seller_access_token
from app.api.schemas.seller import SellerCreate, SellerRead
from app.config import app_settings
from app.utils import TEMPLATE_DIR
from redis_conn import add_jti_to_blacklist

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


### Verify Seller Email
@router.get("/verify")
async def verify_seller_email(token: str, service: SellerServiceDep):
    await service.verify_email(token)
    return {"detail": "Account verified"}


### Email Password Reset Link
@router.get("/forgot_password")
async def forgot_password(email: EmailStr, service: SellerServiceDep):
    await service.send_password_reset_link(email, router.prefix)
    return {"detail": "Check email for password reset link"}


### Password Reset Form
@router.get("/reset_password_form")
async def get_reset_password_form(request: Request, token: str):
    templates = Jinja2Templates(TEMPLATE_DIR)

    return templates.TemplateResponse(
        request=request,
        name="password/reset.html",
        context={
            "reset_url": f"http://{app_settings.APP_DOMAIN}{router.prefix}/reset_password?token={token}"
        },
    )


### Reset Seller Password
@router.post("/reset_password")
async def reset_password(
    request: Request,
    token: str,
    password: Annotated[str, Form()],
    service: SellerServiceDep,
):
    is_success = await service.reset_password(
        token,
        password,
    )

    templates = Jinja2Templates(TEMPLATE_DIR)

    return templates.TemplateResponse(
        request=request,
        name="password/reset_success.html" if is_success else "password/reset_failed.html",
    )


### Logout the seller
@router.get("/logout")
async def logout_seller(
    token_data: Annotated[dict, Depends(get_seller_access_token)],
):
    await add_jti_to_blacklist(token_data["jti"])
    return {"detail": "Successfully logged out"}
