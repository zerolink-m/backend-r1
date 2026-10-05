# app/routers/files.py
from app.utils import (
    require_authorization,
    CursedResponser,
    codes,
    model_to_dict,
    models_to_dict,
    now,
    apply_query_params
)
from app import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from sqlalchemy.exc import IntegrityError
from app.schemas import QueryParams, CreateDatacenter
from fastapi import (
    APIRouter,
    Depends,
    Request
)
from app.models import (
    Subscription,
    UserRole,
    Datacenter
)

from app.services import (
    update_datacenter_client,
    delete_datacenter_client
)
from app.schemas import EditDatacenter


router = APIRouter(
    prefix="/v1/files",
    tags=["files"]
)


@router.put("")
async def upload_file(
    request: Request,
    auth: dict = Depends(require_authorization(required_roles=["user", "support", "admin"]))
):
    async for chunk in request.stream():
        return
    return