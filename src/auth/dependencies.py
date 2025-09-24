from typing import Optional, Annotated
from fastapi import Depends, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .models import User
from src.auth.service import AuthService
from src.db.main import get_session
from .utils import verify_access_token, verify_refresh_token
from fastapi.exceptions import HTTPException
from abc import ABC, abstractmethod
from src.db.redis import token_in_blocklist
from sqlmodel.ext.asyncio.session import AsyncSession


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


async def get_current_user_from_token(token_details: Annotated[HTTPAuthorizationCredentials, Depends(AccessTokenBearer())],
                                      session: AsyncSession = Depends(get_session)) -> Optional[User]:
    user_data = verify_access_token(token_details.credentials)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user_email = user_data.get("user", {}).get("email")
    user = await AuthService().get_user_by_email(user_email, session)
    return user
