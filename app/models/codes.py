# app/models/codes.py
'''
CREATE TABLE codes (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    type ENUM(CodeType) NOT NULL,
    code VARCHAR(8) NOT NULL UNIQUE,
    used BOOL NOT NULL DEFAULT false,
    expires_at BIGINT NOT NULL,
    added_by BIGINT NOT NULL,
    updated_at BIGINT NOT NULL,
    added_at BIGINT NOT NULL
)
'''

from enum import Enum

from sqlalchemy import Enum as SAEnum, String, Boolean, Integer, false, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class CodeType(str, Enum):
    email_confirmation = "email_confirmation"
    email_change = "email_change"
    password_change = "password_change"
    delete_account = "delete_account"


class Code(Base):
    __tablename__ = "codes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    type: Mapped[CodeType] = mapped_column(
        SAEnum(CodeType),
        nullable=False
    )

    code: Mapped[str] = mapped_column(
        String(8),
        nullable=False,
        unique=True
    )

    used: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=false()
    )

    expires_at: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )
    
    added_by: Mapped[int] = mapped_column(
        BigInteger,
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
