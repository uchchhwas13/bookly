from fastapi import APIRouter, Depends
from src.dependencies import get_current_user_from_token
from src.models.user import User
from src.schemas.review import ReviewCreateModel, ReviewModel
from src.services.review_service import ReviewService
from ..db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated

review_router = APIRouter()
review_service = ReviewService()


@review_router.post('/book/{book_uid}', response_model=ReviewModel)
async def add_review_to_books(
    book_uid: str,
    current_user: Annotated[User, Depends(get_current_user_from_token)],
    review_data: ReviewCreateModel,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    print("add_review_to_books called")
    new_review = await review_service.add_review_to_book(current_user.email, book_uid, review_data, session)

    return new_review
