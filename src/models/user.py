# from __future__ import annotations
from typing import List
from datetime import datetime, date
from sqlmodel import Relationship, SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import String
from sqlalchemy.sql import func
import uuid
from typing import Optional


class User(SQLModel, table=True):
    __tablename__ = 'users'

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool = False
    password_hash: str = Field(exclude=True)
    refresh_token: Optional[str] = Field(
        sa_column=Column(String, nullable=True)
    )
    role: str = Field(sa_column=Column(
        pg.VARCHAR, nullable=False, server_default="user"
    ))
    created_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, server_default=func.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, server_default=func.now(),
                                                  onupdate=func.now()))
    reviews: List["Review"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: uuid.UUID = Field(foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, server_default=func.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, server_default=func.now(),
                                                  onupdate=func.now()))
    reviews: List["Review"] = Relationship(
        back_populates="book", sa_relationship_kwargs={"lazy": "selectin"})

    def __repr__(self) -> str:
        return f"<Book {self.title}>"


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
