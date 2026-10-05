# app/schemas/files.py
from app.schemas import DataBaseModel
from typing import Optional
from pydantic import Field, AnyHttpUrl, StringConstraints
from app.models import FileStorageType
from typing import Annotated, Optional
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

class EditFile(DataBaseModel):
    user_id: Optional[int] = Field(ge=1, le=2147483647)
    type: Optional[FileStorageType] = Field()
'''

FilenamePattern = Annotated[
    Optional[str],
    # Любые символы (в т.ч. . ( ) ? * : % ; ! " @ # $ ^ + = | } ] { [ ' и т.д.),
    # кроме управляющих символов и слешей (защита от path traversal)
    StringConstraints(pattern=r"^[^\x00-\x1f/\\]+$", max_length=255)
]