from src.models.review import Review
from src.schemas.review import ReviewCreateModel
from .auth_service import AuthService
from .book_service import BookService
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import status


class ReviewService:
    book_service = BookService()
    auth_service = AuthService()

    async def add_review_to_book(self, user_email: str, book_uid: str, review_data: ReviewCreateModel, session: AsyncSession) -> Review:
        try:
            book = await self.book_service.get_book(book_uid, session)
            user = await self.auth_service.get_user_by_email(user_email, session)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
            review_data_dict = review_data.model_dump()
            new_review = Review(**review_data_dict)
            new_review.user = user
            new_review.book = book

            session.add(new_review)
            await session.commit()
            return new_review
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong"
            )
