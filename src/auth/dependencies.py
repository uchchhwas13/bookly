from typing import Optional
from fastapi import Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .utils import verify_access_token, verify_refresh_token
from fastapi.exceptions import HTTPException
from abc import ABC, abstractmethod
from src.db.redis import token_in_blocklist


class TokenBearer(HTTPBearer, ABC):

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        creds = await super().__call__(request)
        if creds is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        if not await self.validate_token(creds.credentials):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired Token"
            )
        return creds

    @abstractmethod
    async def validate_token(self, token: str) -> bool:
        ...


class AccessTokenBearer(TokenBearer):
    async def validate_token(self, token: str) -> bool:
        token_data = verify_access_token(token)
        if not token_data:
            return False
        jti = token_data.get("jti")
        if not jti:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Invalid token payload",
                        "resolution": "Request a new token"}
            )
        if await token_in_blocklist(jti):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                "error": "This token is invalid or revoked",
                "resolution": "please get new token"
            })
        return True


class RefreshTokenBearer(TokenBearer):
    async def validate_token(self, token: str) -> bool:
        token_data = verify_refresh_token(token)
        if not token_data:
            return False
        jti = token_data.get("jti")
        if not jti:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Invalid token payload",
                        "resolution": "Request a new token"}
            )
        if await token_in_blocklist(jti):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                "error": "This token is invalid or revoked",
                "resolution": "please get new token"
            })
        return True
