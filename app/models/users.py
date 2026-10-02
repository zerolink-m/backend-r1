# app/models/users.py
'''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    avatar INTEGER NULL DEFAULT '1',
    name VARCHAR(16) NULL,
    surname VARCHAR(16) NULL,
    balance NUMERIC(10, 2) NOT NULL DEFAULT '0.00',
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM(UserRole) NOT NULL DEFAULT 'guest',
    region ENUM(Regions) NOT NULL DEFAULT 'NO',
    possible_region ENUM(Regions) NOT NULL DEFAULT 'NO',
    blocked BOOL NOT NULL DEFAULT false,
    blocked_reason VARCHAR(255) NULL,
    updated_at BIGINT NOT NULL,
    added_at BIGINT NOT NULL
)
'''

from decimal import Decimal
from enum import Enum
from app.utils import Regions

from sqlalchemy import Enum as SAEnum, BigInteger, Integer, Boolean, false
from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class UserRole(str, Enum):
    support = "support"
    admin = "admin"
    user = "user"
    guest = "guest"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    avatar: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        server_default="1"
    )

    name: Mapped[str | None] = mapped_column(
        String(16),
        nullable=True
    )

    surname: Mapped[str | None] = mapped_column(
        String(16),
        nullable=True
    )

    balance: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        server_default="0.00"
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole),
        nullable=False,
        server_default="guest"
    )

    region: Mapped[Regions] = mapped_column(
        SAEnum(Regions),
        nullable=False,
        server_default="NO"
    )

    possible_region: Mapped[Regions] = mapped_column(
        SAEnum(Regions),
        nullable=False,
        server_default="NO"
    )

    blocked: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=false()
    )

    blocked_reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    updated_at: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    added_at: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )
