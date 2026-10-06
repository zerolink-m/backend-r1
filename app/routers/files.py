# app/routers/files.py
from app.utils import (
    CursedStreamingResponser,
    require_authorization,
    CursedResponser,
    codes,
    model_to_dict,
    models_to_dict,
    now,
    apply_query_params,
    check_resource_access,
    ResourceOperation
)
from app import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from sqlalchemy.exc import IntegrityError
from app.schemas import QueryParams, CreateDatacenter
from fastapi import (
    APIRouter,
    Depends,
    Request,
    Header,
    Query
)
from app.models import (
    File,
    FileStorageType,
    Ticket,
    UserRole
)
from typing import Optional

from config import settings
from app.services import multipart_stream, file_info, make_client
from app.schemas import EditDatacenter, FilenamePattern, Reason
import uuid


router = APIRouter(
    prefix="/v1/files",
    tags=["files"]
)


@router.get("/{file_id}")
async def get_file(
    file_id: int,
    db: AsyncSession = Depends(get_db),
    auth: dict = Depends(require_authorization(required_roles=["guest", "user", "support", "admin"]))
):
    file = (await db.execute(
        select(File).where(File.user_id == auth["user"].id)
    )).scalar_one_or_none()

    if not file:
        raise CursedResponser(
            code=codes.NOT_FOUND,
            error=f"Resource {file_id} not found"
        )
    
    check_resource_access(
        requesting_user=auth["user"],
        resource_owner_id=file.user_id,
        operation=ResourceOperation.GET
    )

    return CursedResponser(
        code = codes.SUCCESS,
        data = {
            "file": model_to_dict(model=file)
        }
    )

@router.get("/{file_id}/download")
async def download_file(
    file_id: int,
    db: AsyncSession = Depends(get_db),
    auth: dict = Depends(require_authorization(required_roles=["guest", "user", "support", "admin"]))
):
    file = (await db.execute(
        select(File).where(File.id == file_id)
    )).scalar_one_or_none()

    if not file:
        return CursedResponser(
            code=codes.OBJECT_NOT_FOUND,
            data={},
            error=f"Object File by File.id == {file_id} not found."
        )

    check_resource_access(
        requesting_user=auth["user"],
        resource_owner_id=file.user_id,
        operation=ResourceOperation.GET
    )

    file_s3 = await file_info(key=file.external_id)

    if file_s3 is None:
        return CursedResponser(
            code=codes.FILE_NOT_FOUND,
            data={},
            error=f"File not found or S3 error."
        )

    async def stream_file():
        response = None
        s3 = None

        try:
            s3 = await make_client().__aenter__()

            response = await s3.get_object(Bucket=settings.s3_bucket, Key=file.external_id)
            async for chunk in response["Body"]:
                yield chunk

        finally:
            if response is not None:
                await response["Body"].close()

            if s3 is not None:
                await s3.__aexit__(None, None, None)

    return CursedStreamingResponser(
        generator=stream_file(),
        media_type=file_s3["content_type"],
        headers={
            "content-length": str(file.size),
            "content-disposition": f'attachment; filename="{file.original_filename}"'
        }
    )

@router.put("")
async def upload_file(
    request: Request,
    storage_type: Optional[FileStorageType] = FileStorageType.s3,
    x_filename: FilenamePattern = Header(default=None, alias="X-Filename"),
    db: AsyncSession = Depends(get_db),
    auth: dict = Depends(require_authorization(required_roles=["user", "support", "admin"]))
):
    if storage_type == FileStorageType.local:
        return CursedResponser(
            code=codes.FUNCTION_NOT_IMPLEMENTED,
            data={},
            error="'local' function is not available"
        )

    filename = str(uuid.uuid4())
    original_filename = x_filename or filename
    key = f"uploads/user-content/{auth["user"].id}/{filename}"

    # request, а не request.stream() — чтобы работала предпроверка по Content-Length
    size, file_format = await multipart_stream(
        key=key,
        stream=request
    )

    new_file = File(
        user_id=auth["user"].id,
        type=storage_type,
        external_id=key,
        filename=filename,
        original_filename=original_filename,
        size=size,
        format=file_format,
        media_type=request.header.get("media-type", "application/octet-stream"),
        added_by=auth["session"].id,
        updated_at=now(),
        added_at=now()
    )
    db.add(new_file)
    try:
        # flush, чтобы ошибки БД поймать здесь, а не на commit в get_db
        await db.flush()
    except IntegrityError:
        await db.rollback()
        return CursedResponser(
            code=codes.DB_ERROR,
            error="Failed to create file record",
            data={}
        )

    return CursedResponser(
        code=codes.CREATED,
        data={
            "file": model_to_dict(model=new_file)
        }
    )
