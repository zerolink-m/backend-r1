# app/routers/datacenters.py
from app.utils import (
    require_authorization,
    check_resource_access,
    ResourceOperation,
    CursedResponser,
    CursedException,
    CursedStreamingResponser,
    codes,
    model_to_dict,
    models_to_dict,
    check_fields,
    now,
    hash_password,
    verify_password,
    apply_query_params,
    CursedJSON
)
from app import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.schemas import QueryParams
from fastapi import APIRouter, Depends, Query
from app.models import (
    User,
    UserRole,
    Ticket,
    File,
    FileFormat,
    Session,
    Message,
    Message_Files,
    Subscription,
    PayHistory,
    Code,
    Packet
)
from app.services import (
    delete_file
)
import botocore
from app.schemas import EditUser, CreateUser, Reason

