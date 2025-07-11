from typing import Type

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.database.models import User
from app.services.base import BaseService
from app.utils import generate_access_token

password_context = CryptContext(schemes="bcrypt")


class UserService(BaseService):
    def __init__(self, model: Type[User], session: AsyncSession):
        self.model = model
        self.session = session

    async def _add_user(self, data: dict):
        user = self.model(
            **data,
            # Hashed password
            password_hash=password_context.hash(data["password"]),
        ) # type: ignore
        return await self._add(user)

    async def _get_by_email(self, email) -> User | None:
        # metodo scalar retorna apenas a primeira coluna
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )

    async def _generate_token(self, email, password) -> str:
        # Validate the credentials
        user = await self._get_by_email(email)

        if user is None or not password_context.verify(
            password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or password is incorrect",
            )

        return generate_access_token(
            data={
                "user": {
                    "name": user.name,
                    "id": str(user.id),
                }
            },
        )
