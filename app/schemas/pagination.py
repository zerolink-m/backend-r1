# app/schemas/pagination.py
from typing import Optional
from pydantic import BaseModel, Field, model_validator
from app.utils.search import SearchMethod
import logging

class PaginationParams(BaseModel):
    limit: int = Field(default=10, ge=1, le=255, description="Number of items to return per page")
    offset: int = Field(default=0, ge=0, description="Number of items to skip before starting to collect the result set")

class SearchParams(BaseModel):
    search: Optional[str] = Field(default=None, description="Search term to filter results")
    search_column: Optional[str] = Field(default=None, description="Column to search in")
    search_method: SearchMethod = Field(default=SearchMethod.CONTAINS, description="Method to use for searching (equals or contains)")

    @model_validator(mode="after")
    def validate_search_fields(self):
        logging.debug(f"validate_search_fields called with search={self.search}, search_column={self.search_column}")
        if self.search is not None and self.search_column is None:
            raise ValueError("search_column is required when search is provided or search_column is provided")
        return self

class QueryParams(PaginationParams, SearchParams):
    pass