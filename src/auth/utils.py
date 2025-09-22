from datetime import datetime, timedelta
from typing import Any
import uuid
import jwt
from passlib.context import CryptContext
from src.config import config
import logging

password_context = CryptContext(schemes=["bcrypt"])
ACCESS_TOKEN_EXPIRY_DURATION = 300
REFRESH_TOKEN_EXPIRY_DURATION = 3600


def generate_password_hash(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return password_context.verify(password, hash)


def create_access_token(user_data: dict[str, str]) -> str:
    payload: dict[str, Any] = {
        "user": user_data,
        "exp": datetime.now() + timedelta(seconds=ACCESS_TOKEN_EXPIRY_DURATION),
        "refresh": False,
        "jti": str(uuid.uuid4())
    }

    token = jwt.encode(
        payload,
        key=config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM,
    )
    return token


def create_refresh_token(user_data: dict[str, str]) -> str:
    payload: dict[str, Any] = {
        "user": user_data,
        "exp": datetime.now() + timedelta(seconds=REFRESH_TOKEN_EXPIRY_DURATION),
        "refresh": True,
        "jti": str(uuid.uuid4())
    }
    token: str = jwt.encode(
        payload,
        key=config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM,
    )
    return token


def decode_token(token: str) -> dict[str, Any] | None:
    try:
        token_data: dict[str, Any] = jwt.decode(
            jwt=token,
            key=config.JWT_SECRET_KEY,
            algorithms=[config.JWT_ALGORITHM],
        )
        return token_data
    except jwt.PyJWTError as error:
        logging.exception(error)
        return None
