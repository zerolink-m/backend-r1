# app/utils/query_builder.py
from typing import Type, Optional, TYPE_CHECKING
from sqlalchemy import Select
from sqlalchemy.orm import DeclarativeBase
from app.utils.search import SearchMethod
import logging

if TYPE_CHECKING:
    # Только для статической типизации — в рантайм не импортируем,
    # чтобы избежать циклического импорта app.schemas <-> app.utils
    from app.schemas.pagination import QueryParams


def apply_query_params(query: Select, model: Type[DeclarativeBase], params: "QueryParams", searchable_columns: Optional[list[str]] = None) -> Select:
    """
    Apply pagination and search parameters to a SQLAlchemy query.

    :param query: The initial SQLAlchemy query.
    :param model: The SQLAlchemy model class.
    :param params: The QueryParams object containing pagination and search parameters.
    :param searchable_columns: A list of columns that are allowed for searching.
    :return: The modified SQLAlchemy query with applied parameters.
    """
    logging.debug(f"apply_query_params called for model={model.__name__}, params={params}, searchable_columns={searchable_columns}")
    if params.search and params.search_column:
        if not hasattr(model, params.search_column):
            logging.debug(f"Column '{params.search_column}' does not exist in model '{model.__name__}'")
            raise ValueError(f"Column '{params.search_column}' does not exist in model '{model.__name__}'.")

        if searchable_columns and params.search_column not in searchable_columns:
            logging.debug(f"Column '{params.search_column}' is not allowed for searching")
            raise ValueError(f"Column '{params.search_column}' is not allowed for searching.")

        column = getattr(model, params.search_column)

        if params.search_method == SearchMethod.EQUALS:
            logging.debug(f"Applying EQUALS filter on {params.search_column} = {params.search}")
            query = query.where(column == params.search)
        elif params.search_method == SearchMethod.CONTAINS:
            logging.debug(f"Applying CONTAINS filter on {params.search_column} ilike %{params.search}%")
            query = query.where(column.ilike(f"%{params.search}%"))

    logging.debug(f"Applying limit={params.limit}, offset={params.offset}")
    query = query.limit(params.limit).offset(params.offset)

    return query