from typing import Optional
from fastapi import Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .utils import verify_access_token, verify_refresh_token
from fastapi.exceptions import HTTPException
from abc import ABC, abstractmethod


class TokenBearer(HTTPBearer, ABC):

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        creds = await super().__call__(request)
        if creds is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        if not self.validate_token(creds.credentials):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired Token"
            )
        return creds

    @abstractmethod
    def validate_token(self, token: str) -> bool:
        ...


class AccessTokenBearer(TokenBearer):
    def validate_token(self, token: str) -> bool:
        token_data = verify_access_token(token)
        return True if token_data is not None else False


class RefreshTokenBearer(TokenBearer):
    def validate_token(self, token: str) -> bool:
        token_data = verify_refresh_token(token)
        return True if token_data is not None else False
