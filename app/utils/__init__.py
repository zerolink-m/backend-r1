# app/utils/__init__.py

from .codes import (
    # Успех
    SUCCESS,
    CREATED,
    EDITED,
    PARTIALLY_EDITED,
    DELETED,
    ACCEPTED_FOR_WORK,
    NOT_CHANGED,
    TEMPORARY_REDIRECTED,
    AUTHORIZED,
    REDIRECTED,
    STREAMING_RESPONSE,
    # Ошибка
    VALIDATION_ERROR,
    TOKEN_ERROR,
    TOKEN_EXPIRED,
    TOKEN_SIGN_INCORRECT_KEY,
    TOKEN_HAS_INCORRECT_ALGORITHM,
    FORBIDDEN,
    FORBIDDEN_ROLE,
    FORBIDDEN_RESOURCE,
    BAD_REQUEST,
    METHOD_NOT_ALLOWED,
    CONFLICT,
    OBJECT_FIELD_EXISTS,
    TOO_LARGE,
    BAD_GATEWAY,
    DB_ERROR,
    RATE_LIMITED,
    SERVICE_UNAVAILABLE,
    SERVICE_OVERLOADED,
    FIELDS_INCORRECT_AUTHORIZATION_ERROR,
    NOT_FOUND,
    INTERNAL_SERVER_ERROR,
    # Маппинги
    HTTP_MAP,
    DETAILS_MAP,
    http_map,
    detail_map
)
from .regions import REGIONS, Regions
from .logger import setup_logging
from .query_builder import apply_query_params
from .response import CursedResponser, CursedException, CursedStreamingResponser, CursedJSON
from .search import SearchMethod
from .password import hash_password, verify_password
from .helpers import now, model_to_dict, models_to_dict
from .authorization import (
    require_authorization,
    create_token,
    decode_token,
    create_cdn_token,
    check_resource_access,
    ResourceOperation,
    check_fields
)

__all__ = [
    # Коды успеха
    "SUCCESS",
    "CREATED",
    "EDITED",
    "PARTIALLY_EDITED",
    "DELETED",
    "ACCEPTED_FOR_WORK",
    "NOT_CHANGED",
    "TEMPORARY_REDIRECTED",
    "AUTHORIZED",
    "REDIRECTED",
    "STREAMING_RESPONSE",
    # Коды ошибок
    "VALIDATION_ERROR",
    "TOKEN_ERROR",
    "TOKEN_EXPIRED",
    "TOKEN_SIGN_INCORRECT_KEY",
    "TOKEN_HAS_INCORRECT_ALGORITHM",
    "FORBIDDEN",
    "FORBIDDEN_ROLE",
    "FORBIDDEN_RESOURCE",
    "BAD_REQUEST",
    "METHOD_NOT_ALLOWED",
    "CONFLICT",
    "OBJECT_FIELD_EXISTS",
    "TOO_LARGE",
    "BAD_GATEWAY",
    "DB_ERROR",
    "RATE_LIMITED",
    "SERVICE_UNAVAILABLE",
    "SERVICE_OVERLOADED",
    "FIELDS_INCORRECT_AUTHORIZATION_ERROR",
    "NOT_FOUND",
    "INTERNAL_SERVER_ERROR",
    # Маппинги
    "HTTP_MAP",
    "DETAILS_MAP",
    "http_map",
    "detail_map",
    # Логгер
    "setup_logging",
    # Резпонз
    "CursedResponser",
    "CursedStreamingResponser",
    # Поиск
    "SearchMethod",
    "apply_query_params",
    "CursedException",
    "now",
    "model_to_dict",
    "models_to_dict",
    "require_authorization",
    "create_token",
    "decode_token",
    "create_cdn_token",
    "check_resource_access",
    "ResourceOperation",
    "chech_fields",
    "hash_password",
    "verify_password",
    # Regions
    "REGIONS",
    "Regions",
    "CursedJSON"
]
