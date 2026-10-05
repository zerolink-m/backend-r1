# app/schemas/tariffs.py
from app.schemas import DataBaseModel
from typing import Optional
from pydantic import Field, AnyHttpUrl
from app.models import TariffType

from decimal import Decimal


class CreateTariff(DataBaseModel):
    name: str = Field(default="Example tariff", max_length=48)
    description: str = Field(default=None, max_length=64)
    price: Decimal = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    is_available: bool = Field(default=None)
    type: TariffType = TariffType.traffic
    traffic: int = Field(default=None, ge=1, le=9223372036854775807)
    unlimited_time: int = Field(default=None, ge=1, le=9223372036854775807)
    updated_at: int = Field(default=None, ge=1, le=9223372036854775807)
    added_at: int = Field(default=None, ge=1, le=9223372036854775807)

class EditTariff(DataBaseModel):
    name: Optional[str] = Field(default=None, max_length=48)
    description: Optional[str] = Field(default=None, max_length=64)
    price: Optional[Decimal] = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    is_available: Optional[bool] = Field(default=None)
    type: Optional[TariffType] = TariffType.traffic
    traffic: Optional[int] = Field(default=None, ge=1, le=9223372036854775807)
    unlimited_time: Optional[int] = Field(default=None, ge=1, le=9223372036854775807)
    updated_at: Optional[int] = Field(default=None, ge=1, le=9223372036854775807)
    added_at: Optional[int] = Field(default=None, ge=1, le=9223372036854775807)
