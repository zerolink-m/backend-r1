# app/routers/tariffs.py
from app.routers.datacenters import PRIVATE_FIELDS
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
    Tariff
)

from app.services import update_datacenter_client, delete_datacenter_client
from app.schemas import EditDatacenter

router = APIRouter(
    prefix="/v1/tariffs",
    tags=["tariffs"]
)

ALLOWED_FIELDS = [
    "id",
    "name",
    "description",
    "price",
    "is_available",
    "type",
    "traffic",
    "unlimited_until",
    "updated_at",
    "added_at"
]
SEARCHABLE_COLUMNS = [
    "id",
    "name",
    "description",
    "price",
    "is_available",
    "type",
    "traffic",
    "unlimited_until",
    "updated_at",
    "added_at"
]

# готов
@router.get("/{tariff_id}")
async def get_tariff(
    tariff_id: int,
    db: AsyncSession = Depends(get_db)
):
    tariff = (await db.execute(
        select(Tariff).where(Tariff.id == tariff_id)
    )).scalar_one_or_none()

    if tariff is None:
        return CursedResponser(
            code=codes.OBJECT_NOT_FOUND,
            data={},
            error=f"Tariff {tariff_id} not found."
        )

    return CursedResponser(
        code=codes.SUCCESS,
        data={
            "tariff": model_to_dict(model=tariff)
        }
    )

# готов
@router.get("")
async def get_tariffs(
    params: QueryParams,
    db: AsyncSession = Depends(get_db)
):
    query = apply_query_params(
        query=select(Tariff),
        model=Tariff,
        params=params,
        searchable_columns=SEARCHABLE_COLUMNS
    )

    tariffs = (await db.execute(
        query
    )).scalars().all()

    return CursedResponser(
        code = codes.SUCCESS,
        data = {
            "tariffs": models_to_dict(models=tariffs)
        }
    )


