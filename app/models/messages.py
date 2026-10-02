# app/models/messages.py
'''
CREATE TABLE messages (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    ticket_id INTEGER NOT NULL,
    text VARCHAR(4096) NOT NULL,
    updated_at BIGINT NOT NULL,
    added_by BIGINT NOT NULL,
    added_at BIGINT NOT NULL
)

CREATE TABLE messages_files (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    message_id BIGINT NOT NULL,
    file_id INTEGER NOT NULL
)
'''

from sqlalchemy import BigInteger, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    ticket_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    text: Mapped[str] = mapped_column(
        String(4096),
        nullable=False,
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

class Message_Files(Base):
    __tablename__ = "messages_files"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    message_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    file_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )