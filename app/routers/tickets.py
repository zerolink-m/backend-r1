# /app/routers/tickets.py
from app.utils import (
    require_authorization,
    check_resource_access,
    ResourceOperation,
    CursedResponser,
    codes,
    model_to_dict,
    models_to_dict,
    check_fields,
    apply_query_params
)
from app import get_db, db_delete_object
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas import QueryParams
from fastapi import APIRouter, Depends, Query
from app.models import User, UserRole, Ticket
from app.schemas import EditUser


router = APIRouter(
    prefix="/v1/tickets",
    tags=["tickets"]
)

SEARCHABLE_COLUMNS = [
    "id",
    "user_id",
    "subject",
    "status",
    "priority",
    "support_id",
    "resolved_at",
    "updated_at",
    "added_by",
    "added_at",
]
ALLOWED_FIELDS = []

@router.get("/{ticket_id}")
async def get_ticket(
    ticket_id: int,
    db: AsyncSession = Depends(get_db),
    auth: dict = Depends(require_authorization(required_roles=["guest", "user", "support", "admin"]))
):
    ticket = (await db.execute(
        select(Ticket).where(Ticket.id == ticket_id)
    )).scalar_one_or_none()

    check_resource_access(
        requesting_user=auth["user"],
        resource_owner_id=[ticket.support_id, ticket.added_by],
        operation=ResourceOperation.GET
    )

    return CursedResponser(
        code=codes.SUCCESS,
        data={"ticket": model_to_dict(ticket)},
    )

@router.get("")
async def get_tickets(
    params: QueryParams,
    db: AsyncSession = Depends(get_db),
    auth: dict = Depends(require_authorization(required_roles=["guest", "user", "support", "admin"]))
):
    tickets_query = apply_query_params(
        query=select(Ticket),
        model=Ticket,
        params=params,
        searchable_columns=SEARCHABLE_COLUMNS
    )
    if auth["user"].role == UserRole.ADMIN:
        tickets_query = tickets_query
    elif auth["user"].role == UserRole.SUPPORT:
        tickets_query = tickets_query.where(Ticket.support_id == auth["user"].id)
    else:
        tickets_query = tickets_query.where(Ticket.added_by == auth["user"].id)

    tickets = await db.execute(tickets_query).scalars().all()
    return CursedResponser(
        code=codes.SUCCESS,
        data={"tickets": models_to_dict(tickets)}
    )

@router.patch("/{ticket_id}")
async def edit_ticket(
    ticket_id: int,
    db: AsyncSession = Depends(get_db),
    auth: dict = Depends(require_authorization(required_roles=["guest", "user", "support", "admin"]))
):
    return