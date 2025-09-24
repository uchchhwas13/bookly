from __future__ import annotations
from typing import List
from datetime import datetime
from sqlmodel import Relationship, SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from sqlalchemy.sql import func
from typing import Optional
from sqlalchemy import String

from src.models.review import Review


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
    reviews: List[Review] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})

    def __repr__(self) -> str:
        return f"<User {self.username}>"
