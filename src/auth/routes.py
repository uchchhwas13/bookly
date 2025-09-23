from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from src.db.redis import add_jti_to_blocklist
from .schemas import LogOutResponse, LoginResponse, RefreshTokenResponse, UserCreateModel, UserModel, UserLoginModel, UserResponse
from .service import AuthService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import create_access_token, verify_access_token, verify_password, create_refresh_token, verify_refresh_token
from .dependencies import AccessTokenBearer, RefreshTokenBearer

auth_router = APIRouter()
auth_service = AuthService()


@auth_router.post('/signup', response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exists = await auth_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="user with this email already exists")

    new_user = await auth_service.create_user(user_data, session)
    return new_user


@auth_router.post('/login', response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login_user(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    user = await auth_service.get_user_by_email(email, session)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        if password_valid:
            access_token = create_access_token(user_data={
                'email': user.email,
                'user_uid': str(user.uid)
            })

            refresh_token = create_refresh_token(
                user_data={
                    'email': user.email,
                    'user_uid': str(user.uid)
                }
            )
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


@auth_router.post('/refresh-access-token', response_model=RefreshTokenResponse)
async def refresh_access_token(token_details: HTTPAuthorizationCredentials = Depends(RefreshTokenBearer())):
    user_data = verify_refresh_token(token_details.credentials)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired refresh token")
    user_data = user_data.get("user")
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token payload")
    new_access_token = create_access_token(user_data)
    return RefreshTokenResponse(access_token=new_access_token)


@auth_router.post('/logout', response_model=LogOutResponse, status_code=status.HTTP_200_OK)
async def log_out_user(token_details: HTTPAuthorizationCredentials = Depends(AccessTokenBearer())):
    user_data = verify_access_token(token_details.credentials)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired access token")
    jti = user_data['jti']
    await add_jti_to_blocklist(jti)
    return LogOutResponse(message="Logged out successfully")
