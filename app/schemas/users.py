from decimal import Decimal

from pydantic import BaseModel, Field, create_model
from app.utils import Regions
from app.models import UserRole
from typing import TypeVar, Generic, Optional
from enum import Enum


T = TypeVar('T')


class DataWrapper(BaseModel, Generic[T]):
    data: T


class DataBaseModel(BaseModel):
    @classmethod
    def wrap(cls) -> type[BaseModel]:
        """Возвращает класс-обертку для использования в эндпоинтах"""
        return create_model(f"{cls.__name__}Wrapper", data=(cls, ...))

class Reason(str, Enum):
    ticket = "ticket"

class EditUser(DataBaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=16)
    surname: Optional[str] = Field(default=None, min_length=1, max_length=16)
    balance: Decimal = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    region: Regions = Field(default=None)
    possible_region: Regions = Field(default=None)
    email: str = Field(default=None, min_length=1, max_length=255)
    password: str = Field(default=None, min_length=1, max_length=255)
    # Требуется при смене password (для не-админов): подтверждение текущего пароля
    old_password: Optional[str] = Field(default=None, min_length=1, max_length=255)
    avatar: Optional[int] = Field(default=None, ge=1)
    role: UserRole = Field(default=None)
    blocked: bool = Field(default=None)
    blocked_reason: Optional[str] = Field(default=None, min_length=1, max_length=255)
    updated_at: int = Field(default=None, ge=1, le=9223372036854775807)
    added_at: int = Field(default=None, ge=1, le=9223372036854775807)

class CreateUser(DataBaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=16)
    surname: Optional[str] = Field(default=None, min_length=1, max_length=16)
    balance: Decimal = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    region: Regions = Field(default=None)
    possible_region: Regions = Field(default=None)
    email: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=255)
    avatar: Optional[int] = Field(default=None, ge=1)
    role: UserRole = Field(default=None)
    blocked: bool = Field(default=None)
    blocked_reason: Optional[str] = Field(default=None, min_length=1, max_length=255)
    updated_at: int = Field(default=None, ge=1, le=9223372036854775807)
    added_at: int = Field(default=None, ge=1, le=9223372036854775807)