from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
from uuid import uuid4

from app.config import security_settings

APP_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = APP_DIR/"templates"

# Gerando Token
def generate_access_token(
    data: dict,
    expiry: timedelta = timedelta(days=1),
) -> str:

    return jwt.encode(
        payload={
            **data,
            "jti": str(uuid4()),
            "exp": datetime.now(timezone.utc) + expiry,
        },
        algorithm=security_settings.JWT_ALGORITHM,
        key=security_settings.JWT_SECRET,
    )


# Decodificando o Token
def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            jwt=token,
            key=security_settings.JWT_SECRET,
            algorithms=[security_settings.JWT_ALGORITHM],
        )
    except jwt.PyJWTError:
        return None
