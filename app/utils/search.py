# app/utils/search.py
from enum import Enum

class SearchMethod(str, Enum):
    EQUALS = "equals" # По типу "равно" WHERE column = value
    CONTAINS = "contains" # По типу "содержит" WHERE column = %value%

