# app/models/packets.py
'''
CREATE TABLE packets (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    type ENUM(TariffType) NOT NULL DEFAULT 'traffic',
    traffic BIGINT NOT NULL DEFAULT '0',
    unlimited_until BIGINT NULL,
    used_traffic BIGINT NOT NULL DEFAULT '0',
    updated_at BIGINT NOT NULL,
    added_at BIGINT NOT NULL
)
'''
from enum import Enum

from sqlalchemy import BigInteger, Enum as SAEnum, String, Integer, Boolean, true, false
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from app.models import (
    TariffType
)

class Packet(Base):
    __tablename__ = "packets"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    type: Mapped[TariffType] = mapped_column(
        SAEnum(TariffType),
        nullable=False,
        server_default="traffic"
    )

    traffic: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default="0"
    )

    unlimited_until: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    used_traffic: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
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
