# app/models/sessions.py
'''
CREATE TABLE sessions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    ip VARCHAR(64) NOT NULL,
    ua VARCHAR(255) NOT NULL,
    language VARCHAR(12) NOT NULL DEFAULT 'en',
    resolution VARCHAR(11) NULL,
    time_zone VARCHAR(8) NOT NULL DEFAULT '0',
    last_login BIGINT NOT NULL,
    last_ip VARCHAR(64) NOT NULL,
    updated_at BIGINT NOT NULL,
    added_at BIGINT NOT NULL
)
'''

from sqlalchemy import String, Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    ip: Mapped[str] = mapped_column(
        String(64),
        nullable=False
    )

    ua: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    language: Mapped[str] = mapped_column(
        String(12),
        nullable=False,
        server_default="en"
    )

    resolution: Mapped[str | None] = mapped_column(
        String(11),
        nullable=True
    )

    time_zone: Mapped[str] = mapped_column(
        String(8),
        nullable=False,
        server_default="0"
    )

    last_login: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    last_ip: Mapped[str] = mapped_column(
        String(64),
        nullable=False
    )

    updated_at: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    added_at: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )
