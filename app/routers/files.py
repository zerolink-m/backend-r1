# app/routers/files.py
from app.utils import (
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

from app.services import multipart_stream
from app.schemas import EditDatacenter, FilenamePattern, Reason
import uuid


router = APIRouter(
    prefix="/v1/files",
    tags=["files"]
)


@router.get("/{file_id}")
async def get_file(
    file_id: int,
    reason: Reason | None = Query(default=None, max_length=64),
    reason_value: int | None = Query(default=None, ge=1),
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
    '''
    if reason == Reason.ticket and reason_value is not None:
        ticket = (await db.execute(
            select(Ticket).where(Ticket.id == reason_value)
        )).scalar_one_or_none()

        # Если тикета нет
        if ticket is None:
            return CursedResponser(
                code=codes.FORBIDDEN_RESOURCE,
                data={},
                error=f"Ticket {reason_value} is not exists."
            )
        
        # Если саппорт то должно совпадать лол
        if auth["user"].role == UserRole.SUPPORT:
            if ticket.support_id != auth["user"].id:
                return CursedResponser(
                    code=codes.FORBIDDEN_RESOURCE,
                    data={},
                    error="Bad reason."
                )
            if ticket.user_id != authid:
                return CursedResponser(
                    code=codes.FORBIDDEN_RESOURCE,
                    data={},
                    error="Bad reason."
                )

        # Проверка остальных ролей
        else:
            if ticket.user_id != auth["user"].id:
                return CursedResponser(
                    code=codes.FORBIDDEN_RESOURCE,
                    data={},
                    error="Bad reason."
                )

            if ticket.support_id != user_id:
                return CursedResponser(
                    code=codes.FORBIDDEN_RESOURCE,
                    data={},
                    error="Bad reason."
                )
                      
    else:
        check_resource_access(
            requesting_user=auth["user"],
            resource_owner_id=user_id,
            operation=ResourceOperation.GET
        )
    '''
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
    
    return

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
