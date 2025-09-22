from datetime import datetime
import uuid
from pydantic import BaseModel, Field, EmailStr


class UserCreateModel(BaseModel):
    first_name: str
    last_name: str
    username: str = Field(max_length=8)
    email: EmailStr
    password: str = Field(min_length=6)


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
