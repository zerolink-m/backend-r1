# app/models/tickets.py
'''
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    subject VARCHAR(128) NOT NULL DEFAULT 'Subject',
    status ENUM(TicketStatus) NOT NULL DEFAULT 'open',
    priority ENUM(TicketPriority) NOT NULL DEFAULT 'medium',
    support_id INTEGER NULL,
    resolved_at BIGINT NULL,
    updated_at BIGINT NOT NULL,
    added_by BIGINT NOT NULL,
    added_at BIGINT NOT NULL
)
'''

from enum import Enum

from sqlalchemy import BigInteger, Integer, Enum as SAEnum, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class TicketStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    waiting = "waiting"
    resolved = "resolved"
    closed = "closed"


class TicketPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    subject: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        server_default="Subject"
    )

    status: Mapped[TicketStatus] = mapped_column(
        SAEnum(TicketStatus),
        nullable=False,
        server_default="open"
    )

    priority: Mapped[TicketPriority] = mapped_column(
        SAEnum(TicketPriority),
        nullable=False,
        server_default="medium"
    )

    support_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    resolved_at: Mapped[int | None] = mapped_column(
        BigInteger,
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
