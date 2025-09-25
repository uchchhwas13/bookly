from fastapi import status, APIRouter, Depends
from fastapi.exceptions import HTTPException
from typing import List, Annotated
from src.models.user import User
from ..schemas.book import BookDetailsModel, BookModel, BookUpdateModel
from ..db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from ..services.book_service import BookService
from ..schemas.book import BookCreateModel
from src.dependencies import AccessTokenBearer, get_current_user_from_token
from fastapi.security import HTTPAuthorizationCredentials

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()


@book_router.get('/', response_model=List[BookDetailsModel], status_code=status.HTTP_200_OK)
async def get_books(session: Annotated[AsyncSession, Depends(get_session)],
                    _: Annotated[HTTPAuthorizationCredentials, Depends(access_token_bearer)],
                    user_uid: str | None = None):
    if user_uid:
        return await book_service.get_user_books(user_uid, session)
    return await book_service.get_all_books(session)


@book_router.post('/', response_model=BookModel, status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: BookCreateModel, session: Annotated[AsyncSession,
                        Depends(get_session)],  current_user: Annotated[User, Depends(get_current_user_from_token)]):
    new_book = await book_service.create_book(current_user.uid, book_data, session)
    return new_book


@book_router.get('/{book_uid}', response_model=BookDetailsModel)
async def get_book(book_uid: str, session: Annotated[AsyncSession, Depends(get_session)],  _: Annotated[HTTPAuthorizationCredentials, Depends(access_token_bearer)]):
    book = await book_service.get_book(book_uid, session)

    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Book not found")


@book_router.patch('/{book_uid}', response_model=BookModel)
async def update_book(book_uid: str, book_update_data: BookUpdateModel, session: Annotated[AsyncSession, Depends(get_session)],  _: Annotated[HTTPAuthorizationCredentials, Depends(access_token_bearer)]):
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Book not found")


@book_router.delete('/{book_uid}', response_model=BookModel)
async def delete_book(book_uid: str, session: Annotated[AsyncSession, Depends(get_session)],  _: Annotated[HTTPAuthorizationCredentials, Depends(access_token_bearer)]):
    deleted_book = await book_service.delete_book(book_uid, session)

    if deleted_book:
        return deleted_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Book not found")
