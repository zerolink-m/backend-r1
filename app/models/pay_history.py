# app/models/pay_history.py
'''
CREATE TABLE pay_history (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    subscription_id INTEGER NULL,
    tariff_id INTEGER NULL,
    status ENUM(PaymentStatus) NOT NULL DEFAULT 'created',
    error VARCHAR(1024) NULL,
    provider ENUM(PaymentProvider) NOT NULL DEFAULT 'from_balance',
    external_id VARCHAR(255) NULL,
    sum NUMERIC(10, 2) NULL,
    updated_at BIGINT NOT NULL,
    added_by BIGINT NOT NULL,
    added_at BIGINT NOT NULL
)
'''

from decimal import Decimal
from enum import Enum

from sqlalchemy import Enum as SAEnum, Numeric, String, Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class PaymentStatus(str, Enum):
    created = "created"
    expired = "expired"
    success = "success"
    error = "error"
    creating_error = "creating_error"


class PaymentProvider(str, Enum):
    admin = "admin"
    from_balance = "from_balance"


class PayHistory(Base):
    __tablename__ = "pay_history"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    subscription_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    tariff_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    status: Mapped[PaymentStatus] = mapped_column(
        SAEnum(PaymentStatus),
        nullable=False,
        server_default="created",
    )

    error: Mapped[str | None] = mapped_column(
        String(1024),
        nullable=True
    )

    provider: Mapped[PaymentProvider] = mapped_column(
        SAEnum(PaymentProvider),
        nullable=False,
        server_default="from_balance"
    )

    external_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    sum: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True
    )

    updated_at: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    added_by: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    added_at: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )
