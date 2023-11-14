from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr
from fastapi_users.schemas import CreateUpdateDictModel


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase, CreateUpdateDictModel):
    first_name: str
    last_name: str
    password: str


class UserUpdate(UserCreate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None


class UserRead(UserBase):
    id: UUID
    full_name: str

    class Config:
        from_attributes = True
