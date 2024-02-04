from typing import Optional
from uuid import UUID

from fastapi_users.schemas import CreateUpdateDictModel
from pydantic import BaseModel, EmailStr


class UserCreate(CreateUpdateDictModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str


class UserUpdate(CreateUpdateDictModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None


class UserRead(BaseModel):
    id: UUID
    full_name: str

    class Config:
        from_attributes = True
