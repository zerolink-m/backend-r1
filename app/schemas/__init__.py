# app/schemas/__init__.py

from .pagination import (
    PaginationParams,
    QueryParams,
    SearchParams,
)
from .users import (
    CreateUser,
    EditUser,
    Regions,
    Reason
)
from .datacenters import(
    EditDatacenter
)

from typing import TypeVar, Generic
from pydantic import BaseModel, create_model

__all__ = [
    # Pagination
    "PaginationParams",
    "QueryParams",
    "SearchParams",
    # Users
    "CreateUser",
    "EditUser",
    "Regions",
    "Reason",
    "EditDatacenter"
]

T = TypeVar('T')


class DataWrapper(BaseModel, Generic[T]):
    data: T


class DataBaseModel(BaseModel):
    @classmethod
    def wrap(cls) -> type[BaseModel]:
        """Возвращает класс-обертку для использования в эндпоинтах"""
        return create_model(f"{cls.__name__}Wrapper", data=(cls, ...))