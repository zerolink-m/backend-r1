# app/utils/authorization.py
from jose import jwt, ExpiredSignatureError, JWTError
from config import settings
from app.utils import CursedException
from app.utils import codes
from fastapi import Request, Depends
from app.models import User, Session, UserRole
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from enum import Enum
import logging
import hashlib
import base64


class ResourceOperation(str, Enum):
    """Типы операций над ресурсами"""
    GET = "get"
    LIST = "list"
    CREATE = "create"
    EDIT = "edit"
    DELETE = "delete"


def create_token(data: dict, token_type: int = 0) -> str:
    logging.debug(f"create_token called with token_type={token_type}, data_keys={list(data.keys())}")
    if token_type == 0: # Access token
        data["type"] = 0
        secret = settings.jwt_access_secret

    elif token_type == 1: # Refresh token
        data["type"] = 1
        secret = settings.jwt_refresh_secret

    else:
        logging.critical(f"Token type: {token_type} not exists, fallback to 0 (access)")
        data["type"] = 0
        secret = settings.jwt_access_secret

    
    token = jwt.encode(
        claims=data,
        key=secret,
        algorithm=settings.jwt_algorithm
    )

    logging.debug(f"create_token generated token of type {data['type']}")
    return token

def decode_token(token: str) -> dict:
    logging.debug("decode_token called")
    unverified_data = jwt.get_unverified_claims(token)
    logging.debug(f"decode_token unverified claims type={unverified_data.get('type')}")
    if unverified_data.get("type") == 0:
        secret = settings.jwt_access_secret

    elif unverified_data.get("type") == 1:
        secret = settings.jwt_refresh_secret

    else:
        secret = settings.jwt_access_secret

    try:
        data = jwt.decode(
            token=token,
            key=secret,
            algorithms=[settings.jwt_algorithm]
        )

    except ExpiredSignatureError as error:
        logging.debug(f"decode_token failed: token expired ({error})")
        raise CursedException(code=codes.TOKEN_EXPIRED, error=str(error))

    except JWTError as error:
        error_msg = str(error).lower()

        if "signature" in error_msg or "verification failed" in error_msg:
            logging.debug(f"decode_token failed: incorrect signature ({error})")
            raise CursedException(code=codes.TOKEN_SIGN_INCORRECT_KEY, error=str(error))

        elif "algorithm" in error_msg:
            logging.debug(f"decode_token failed: incorrect algorithm ({error})")
            raise CursedException(code=codes.TOKEN_HAS_INCORRECT_ALGORITHM, error=str(error))

        else:
            logging.debug(f"decode_token failed: generic JWT error ({error})")
            raise CursedException(code=codes.TOKEN_ERROR, error=str(error))

    except Exception as error:
        logging.debug(f"decode_token failed: unexpected error ({error})")
        raise CursedException(code=codes.TOKEN_ERROR, error=str(error))

    logging.debug("decode_token succeeded")
    return data

def create_cdn_token(path: str, expires: int, ip: str = "") -> str:
    logging.debug(f"create_cdn_token called with path={path}, expires={expires}, ip={ip}")
    raw = f"{settings.s3_cdn_key}{path}{ip}{expires}"

    raw_md5 = hashlib.md5(raw.encode()).digest()
    token = base64.b64encode(raw_md5).decode()

    token = token.replace("/", "_").replace("+", "-").replace("=", "")

    logging.debug(f"create_cdn_token generated token for path={path}")
    return f"md5({token})"

def require_authorization(required_roles: list | None = None, refresh_token_needed: bool = False, public_endpoint: bool | None = False):
    logging.debug(f"require_authorization factory called with required_roles={required_roles}, refresh_token_needed={refresh_token_needed}, public_endpoint={public_endpoint}")
    if required_roles is None:
        required_roles = []

    from app.database import get_db

    async def dependency(request: Request, db: AsyncSession = Depends(get_db)) -> dict | None:
        logging.debug(f"require_authorization dependency called, required_roles={required_roles}, refresh_token_needed={refresh_token_needed}, public_endpoint={public_endpoint}")
        authorization = request.headers.get("Authorization", "")

        # Базовая проверка
        if not authorization:
            if public_endpoint:
                logging.debug("Authorization header is empty on public endpoint")
                return None
            logging.debug("Authorization header is empty")
            raise CursedException(code=codes.TOKEN_ERROR, error="Authorization header is empty.")

        elif not authorization.startswith("Bearer "):
            logging.debug("Authorization header does not start with 'Bearer '")
            raise CursedException(code=codes.TOKEN_ERROR, error="Authorization header need 'Bearer'")

        else:
            token = decode_token(authorization[7::])

        logging.debug(f"Decoded token: id={token.get('id')}, sid={token.get('sid')}, role={token.get('role')}, type={token.get('type')}")

        # Если обязателен рефреш и токен имеет тип 0 - access
        if refresh_token_needed == True and token["type"] == 0:
            logging.debug("Refresh token required but access token provided")
            raise CursedException(code=codes.TOKEN_ERROR, error="Refresh token needed")

        # Если не обязателен рефреш и токен имеет тип 1 - refresh
        if refresh_token_needed == False and token["type"] == 1:
            logging.debug("Access token required but refresh token provided")
            raise CursedException(code=codes.TOKEN_ERROR, error="Access token needed")

        # Если роль не совпадает
        if token["role"] not in required_roles:
            logging.debug(f"Role {token['role']} not in required_roles={required_roles}")
            raise CursedException(code=codes.FORBIDDEN_ROLE, error=f"Role {token['type']} is not allowed")

        # Взять юзера
        logging.debug(f"Querying user with id={token['id']}")
        result = await db.execute(
            select(User).where(User.id == token["id"])
        )
        user = result.scalar_one_or_none()

        if not user:
            logging.debug(f"User with id={token['id']} not found")
            raise CursedException(code=codes.INTERNAL_SERVER_ERROR, error="User not found")

        # Если юзер заблокирован.
        if user.blocked == 1:
            raise CursedException(code=codes.YOU_ARE_BLOCKED, error=f"You are blocked. Reason: {user.blocked_reason}")

        # Взять сессию
        logging.debug(f"Querying session with id={token['sid']}")
        result = await db.execute(
            select(Session).where(Session.id == token["sid"])
        )
        session = result.scalar_one_or_none()

        # Защита от несуществующей сессии
        if not session:
            logging.debug(f"Session with id={token['sid']} not found")
            raise CursedException(code=codes.INTERNAL_SERVER_ERROR, error="Session not found")

        logging.debug(f"Authorization successful for user_id={user.id}, session_id={session.id}")
        return {"user":user, "session": session}

    return dependency

def check_resource_access(
    requesting_user: User,
    resource_owner_id: int | list | None  = None,
    operation: ResourceOperation = ResourceOperation.GET,
    #allow_support: bool = False
) -> None:
    """
    Универсальная проверка прав доступа к ресурсу.

    Args:
        requesting_user: Пользователь, который запрашивает доступ
        resource_owner_id: ID владельца ресурса (None для операций CREATE/LIST) может быть list
        operation: Тип операции (GET, LIST, CREATE, EDIT, DELETE)
        allow_support: Разрешить ли support доступ (по умолчанию False)

    Raises:
        CursedException: Если доступ запрещен

    Логика:
        - ADMIN всегда имеет доступ ко всем ресурсам
        - SUPPORT имеет доступ, если allow_support=True
        - USER может работать только со своими ресурсами (когда resource_owner_id == user.id)
        - Для CREATE и LIST resource_owner_id может быть None
    """
    logging.debug(
        f"check_resource_access: user_id={requesting_user.id}, "
        f"user_role={requesting_user.role}, resource_owner_id={resource_owner_id}, "
        f"operation={operation}"
    )

    # Админ может все
    if requesting_user.role == UserRole.ADMIN:
        logging.debug("Access granted: user is ADMIN")
        return

    # Support может, если разрешено
    #if allow_support and requesting_user.role == UserRole.SUPPORT:
    #    logging.debug("Access granted: user is SUPPORT and allow_support=True")
    #    return

    # Для CREATE и LIST не проверяем владение (там своя логика)
    if operation in (ResourceOperation.CREATE, ResourceOperation.LIST):
        logging.debug(f"Access granted: operation {operation} does not require ownership check")
        return

    # Для GET, EDIT, DELETE проверяем владение
    if resource_owner_id is None:
        logging.error(f"resource_owner_id is None for operation {operation}")
        raise CursedException(
            code=codes.INTERNAL_SERVER_ERROR,
            error=f"Resource owner ID is required for {operation} operation"
        )

    # Проверка владения
    if isinstance(resource_owner_id, int):
        resource_owner_id = [resource_owner_id]
    if requesting_user.id not in resource_owner_id:
        logging.debug(
            f"Access denied: user {requesting_user.id} tried to {operation} "
            f"resource owned by {resource_owner_id}"
        )
        raise CursedException(
            code=codes.FORBIDDEN_RESOURCE,
            error=f"Cannot {operation.value} resource {resource_owner_id}"
        )

    logging.debug(f"Access granted: user owns the resource")

def check_fields(body: dict, allowed_fields: list[str]) -> None:
    unknown = set(body) - set(allowed_fields)
    if unknown:
        raise CursedException(
            code=codes.FIELD_NOT_EDITABLE,
            error=f"These fields {sorted(unknown)} cannot be changed."
        )