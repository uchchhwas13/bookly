from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import UserCreateModel, UserModel
from .service import AuthService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession


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
