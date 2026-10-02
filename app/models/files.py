# app/models/files.py
'''
CREATE TABLE files (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    type ENUM(FileStorageType) NOT NULL DEFAULT 's3',
    external_id VARCHAR(512) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    size INTEGER NOT NULL,
    format ENUM(FileFormat) NOT NULL DEFAULT 'file',
    added_by BIGINT NOT NULL,
    updated_at BIGINT NOT NULL,
    added_at BIGINT NOT NULL
)
'''

from enum import Enum

from sqlalchemy import Enum as SAEnum, String, BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class FileStorageType(str, Enum):
    local = "local"
    s3 = "s3"


class FileFormat(str, Enum):
    image = "image"
    video = "video"
    text = "text"
    file = "file"
    music = "music"
    document = "document"


class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    type: Mapped[FileStorageType] = mapped_column(
        SAEnum(FileStorageType),
        nullable=False,
        server_default="s3"
    )

    external_id: Mapped[str] = mapped_column(
        String(512),
        nullable=False
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    size: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    format: Mapped[FileFormat] = mapped_column(
        SAEnum(FileFormat),
        nullable=False,
        server_default="file"
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
