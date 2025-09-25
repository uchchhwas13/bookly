from pydantic import BaseModel
from datetime import datetime
import uuid


class ReviewCreateModel(BaseModel):
    rating: int
    review_text: str


class ReviewModel(BaseModel):
    uid: uuid.UUID
    rating: int
    review_text: str
    user_uid: uuid.UUID
    book_uid: uuid.UUID
    created_at: datetime
    updated_at: datetime
