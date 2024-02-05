from typing import Optional
from uuid import UUID

from fastapi_users.schemas import CreateUpdateDictModel
from pydantic import BaseModel, ConfigDict, EmailStr


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
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    full_name: str
