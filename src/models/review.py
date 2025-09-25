from sqlmodel import Relationship, SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from src.models.book import Book
from src.models.user import User


class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    rating: int = Field(lt=5)
    review_text: str
    user_uid: uuid.UUID = Field(foreign_key="users.uid")
    book_uid: uuid.UUID = Field(foreign_key="books.uid")
    created_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, server_default=func.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, server_default=func.now(),
                                                  onupdate=func.now()))
    user: User = Relationship(back_populates="reviews")
    book: Book = Relationship(back_populates="reviews")

    def __repr__(self) -> str:
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"
