# app/routers/tariffs.py
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

from app.schemas import (
    QueryParams,
    CreateTariff,
    EditTariff
)
from fastapi import (
    APIRouter,
    Depends
)
from app.models import (
    Tariff,
    TariffType
)


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
    "unlimited_time",
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
    "unlimited_time",
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

@router.post("")
async def create_tariff(
    data: CreateTariff,
    db: AsyncSession = Depends(get_db),
    auth: dict = Depends(require_authorization(required_roles=["admin"]))
):
    data = data.model_dump(exclude_unset=True)
    data["updated_at"] = now()
    data["added_at"] = now()
    if data.get("type", TariffType.traffic) == TariffType.traffic:
        data["unlimited_time"] = None
    elif data.get("type", TariffType.traffic) == TariffType.unlimited:
        data["traffic"] = None

    new_tariff = Tariff(**data)
    db.add(new_tariff)
    await db.flush()

    return CursedResponser(
        code=codes.CREATED,
        data={"tariff": model_to_dict(model=new_tariff)}
    )

@router.patch("/{tariff_id}")
async def edit_tariff(
    data: EditTariff,
    tariff_id: int,
    db: AsyncSession = Depends(get_db),
    auth: dict = Depends(require_authorization(required_roles=["admin"]))
):
    data = data.model_dump(exclude_unset=True)
    tariff = (await db.execute(
        select(Tariff).where(Tariff.id == tariff_id)
    )).scalar_one_or_none()

    if tariff is None:
        return CursedResponser(
            code=codes.OBJECT_NOT_FOUND,
            data={},
            error=f"Tariff {tariff_id} not found."
        )

    data.pop("updated_at", None)
    data.pop("added_at", None)
    data["updated_at"] = now()

    if data.get("type", TariffType.traffic) == TariffType.traffic:
        data["unlimited_time"] = None
    elif data.get("type", TariffType.traffic) == TariffType.unlimited:
        data["traffic"] = None

    for field, value in data.items():
        setattr(tariff, field, value)

    await db.flush()

    return CursedResponser(
        code=codes.EDITED,
        data={
            "tariff": model_to_dict(model=tariff)
        }
    )

@router.delete("/{tariff_id}")
async def delete_tariff(
    tariff_id: int,
    db: AsyncSession = Depends(get_db),
    auth: dict = Depends(require_authorization(required_roles=["admin"]))
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

    await db.delete(tariff)

    return CursedResponser(
        code=codes.DELETED,
        data={
            "tariff": model_to_dict(model=tariff)
        }
    )
