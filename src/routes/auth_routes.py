from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from src.models.user import User
from src.db.redis import add_jti_to_blocklist
from ..schemas.user import LogOutResponse, LoginResponse, TokenPairResponse, TokenRefreshRequest, UserCreateModel, UserModel, UserLoginModel, UserResponse
from ..services.auth_service import AuthService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from ..utils import create_access_token, verify_access_token, verify_password, create_refresh_token, verify_refresh_token
from ..dependencies import AccessTokenBearer, get_current_user_from_token
from typing import Annotated

auth_router = APIRouter()
auth_service = AuthService()


@auth_router.post('/signup', response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: Annotated[AsyncSession, Depends(get_session)]):
    email = user_data.email
    user_exists = await auth_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="user with this email already exists")

    new_user = await auth_service.create_user(user_data, session)
    return new_user


@auth_router.post('/login', response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login_user(login_data: UserLoginModel, session: Annotated[AsyncSession, Depends(get_session)]):
    email = login_data.email
    password = login_data.password

    user = await auth_service.get_user_by_email(email, session)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        if password_valid:
            access_token = create_access_token(user_data={
                'email': user.email,
                'user_uid': str(user.uid),
                'role': user.role
            })

            refresh_token = create_refresh_token(
                user_data={
                    'email': user.email,
                    'user_uid': str(user.uid),
                    'role': user.role
                }
            )

            await auth_service.save_refresh_token(user, refresh_token, session)

            return LoginResponse(
                message="Login successful",
                access_token=access_token,
                refresh_token=refresh_token,
                user=UserResponse(
                    email=user.email,
                    uid=str(user.uid)
                )
            )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid Email or Password"
    )


@auth_router.post('/token/refresh', response_model=TokenPairResponse)
async def refresh_access_token(request_body: TokenRefreshRequest, session: Annotated[AsyncSession, Depends(get_session)]):
    token_payload = verify_refresh_token(request_body.refresh_token)
    if not token_payload:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or expired refresh token"
        )

    user_id = token_payload.get("user", {}).get("user_uid")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token payload"
        )

    tokenResponse = await auth_service.refresh_tokens(
        request_body.refresh_token, user_id, session
    )
    return tokenResponse


@auth_router.post('/logout', response_model=LogOutResponse, status_code=status.HTTP_200_OK)
async def log_out_user(
    token_details: Annotated[HTTPAuthorizationCredentials, Depends(AccessTokenBearer())],
    session: AsyncSession = Depends(get_session),
):
    user_data = verify_access_token(token_details.credentials)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or expired access token"
        )

    jti = user_data['jti']
    await add_jti_to_blocklist(jti)

    await auth_service.remove_refresh_token(user_data.get('user', {}).get('email'), session)

    return LogOutResponse(message="Logged out successfully")


@auth_router.get('/me', response_model=UserModel)
async def get_current_user(user: Annotated[User, Depends(get_current_user_from_token)]):
    return user
