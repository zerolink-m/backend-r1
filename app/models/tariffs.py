# app/models/tariffs.py
'''
CREATE TABLE tariffs (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(48) NOT NULL DEFAULT 'Example tariff',
    description VARCHAR(64) NULL DEFAULT 'Example tariff description',
    price NUMERIC(10, 2) NOT NULL DEFAULT '0',
    is_available BOOL NOT NULL DEFAULT false,
    type ENUM(TariffType) NOT NULL DEFAULT 'traffic',
    traffic BIGINT NULL,
    unlimited_until BIGINT NULL DEFAULT '0',
    updated_at BIGINT NOT NULL,
    added_at BIGINT NOT NULL
)
'''

from decimal import Decimal
from enum import Enum

from sqlalchemy import BigInteger, Integer, Enum as SAEnum, Numeric, String, Boolean, false
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class TariffType(str, Enum):
    unlimited = "unlimited"
    traffic = "traffic"


class Tariff(Base):
    __tablename__ = "tariffs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(48),
        nullable=False,
        server_default="Example tariff"
    )

    description: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        server_default="Example tariff description"
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        server_default="0"
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=false()
    )

    type: Mapped[TariffType] = mapped_column(
        SAEnum(TariffType),
        nullable=False,
        server_default="traffic"
    )

    traffic: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    unlimited_time: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
        server_default="0"
    )

    updated_at: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    added_at: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )
