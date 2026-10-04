# app/routers/datacenters.py
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
    UserRole,
    Datacenter
)

from app.services import update_datacenter_client
from app.schemas import EditDatacenter


router = APIRouter(
    prefix="/v1/datacenters",
    tags=["datacenters"]
)

ALLOWED_FIELDS = [
    "id",
    "location",
    "country",
    "city",
    "guaranted_radius",
    "speed_type",
    "speed",
    "status_url",
    "status",
    "is_available",
    "remnawave_supported",
    "remnawave_url",
    "remnawave_token",
    "remnawave_internal_squad",
    "amnezia_supported",
    "wireguard_supported",
    "wgdashboard_url",
    "wgdashboard_token",
    "wireguard_interface",
    "amnezia_interface",
    "updated_at",
    "added_at"
]
SEARCHABLE_COLUMNS = [
    "id",
    "location",
    "country",
    "city",
    "guaranted_radius",
    "speed_type",
    "speed",
    "status_url",
    "status",
    "is_available",
    "remnawave_supported",
    "amnezia_supported",
    "wireguard_supported",
    "updated_at",
    "added_at"
]
PRIVATE_FIELDS = [
    "remnawave_url",
    "remnawave_token",
    "remnawave_internal_squad",
    "wgdashboard_url",
    "wgdashboard_token",
    "wireguard_interface",
    "amnezia_interface"
]

# публичный эндпоинт, готов
@router.get("/{datacenter_id}")
async def get_datacenter(
    datacenter_id: int,
    db: AsyncSession = Depends(get_db),
    auth: dict = Depends(require_authorization(required_roles=["admin"], public_endpoint=True))
):
    datacenter = (await db.execute(
        select(Datacenter).where(Datacenter.id == datacenter_id)
    )).scalar_one_or_none()

    if datacenter is None:
        return CursedResponser(
            code=codes.DATACENTER_NOT_FOUND,
            data={},
            error=f"Datacenter {datacenter_id} not found."
        )

    if auth is not None:
        if auth["user"].role == UserRole.admin:
            return CursedResponser(
                code=codes.SUCCESS,
                data={
                    "datacenter": model_to_dict(model=datacenter)
                }
            )
    
    else:
        return CursedResponser(
            code=codes.SUCCESS,
            data={
                "datacenter": model_to_dict(model=datacenter, exclude=PRIVATE_FIELDS)
            }
        )   

# готов
@router.get("")
async def get_datacenters(
    params: QueryParams,
    db: AsyncSession = Depends(get_db),
    auth: dict = Depends(require_authorization(required_roles=["admin"], public_endpoint=True))
):
    query = apply_query_params(
        query=select(Datacenter),
        model=Datacenter,
        params=params,
        searchable_columns=SEARCHABLE_COLUMNS
    )

    datacenters = (await db.execute(
        query
    )).scalars().all()

    if auth is not None:
        if auth["user"].role == UserRole.admin:
            return CursedResponser(
                code = codes.SUCCESS,
                data = {
                    "datacenters": models_to_dict(models=datacenters)
                }
            )

    else:
        return CursedResponser(
            code = codes.SUCCESS,
            data = {
                "datacenters": models_to_dict(models=datacenters, exclude=PRIVATE_FIELDS)
            }
        )

# готов
@router.post("")
async def create_datacenter(
    request: Request,
    data: CreateDatacenter,
    db: AsyncSession = Depends(get_db),
    auth: dict = Depends(require_authorization(required_roles=["admin"]))
):
    data = data.model_dump(exclude_unset=True)

    data["updated_at"] = now()
    data["added_at"] = now()

    new_datacenter = Datacenter(**data)
    db.add(new_datacenter)
    await db.flush()

    request.app.state.datacenter_clients = update_datacenter_client(
        datacenter=new_datacenter,
        clients=request.app.state.datacenter_clients
    )

    return CursedResponser(
        code=codes.CREATED,
        data={"datacenter": model_to_dict(model=new_datacenter)}
    )

# готов
@router.patch("/{datacenter_id}")
async def edit_datacenter(
    request: Request,
    datacenter_id: int,
    data: EditDatacenter,
    db: AsyncSession = Depends(get_db),
    auth: dict = Depends(require_authorization(required_roles=["admin"]))
):
    data = data.model_dump(exclude_unset=True)
    datacenter = (await db.execute(
        select(Datacenter).where(Datacenter.id == datacenter_id)
    )).scalar_one_or_none()

    if datacenter is None:
        return CursedResponser(
            code=codes.DATACENTER_NOT_FOUND,
            data={},
            error=f"Datacenter {datacenter_id} not found."
        )

    data.pop("updated_at", None)
    data.pop("added_at", None)
    data["updated_at"] = now()

    if data.migrate_subscriptions == True:
        return CursedResponser(
            code=codes.FUNCTION_NOT_IMPLEMENTED,
            data={},
            error="migrate_subscriptions function is not currently implemented."
        )

    for field, value in data.items():
        setattr(datacenter, field, value)

    await db.flush()

    request.app.state.datacenter_clients = update_datacenter_client(
        datacenter=datacenter,
        clients=request.app.state.datacenter_clients
    )
    
    return CursedResponser(
        code=codes.EDITED,
        data={
            "datacenter": model_to_dict(model=datacenter)
        }
    )

@router.delete("/{datacenter_id}")
async def delete_datacenter(

):
    return
