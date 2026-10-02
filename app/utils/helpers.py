import time
from sqlalchemy.inspection import inspect
from decimal import Decimal
#from config import settings
import logging


def now() -> int:
    result = int(time.time())
    logging.debug(f"now() called, returning {result}")
    return result

def model_to_dict(model, exclude: list[str] | None = None):
    """Конвертирует SQLAlchemy модель в словарь.

    exclude — список имён колонок, которые не включать в результат
    (приватные поля вроде password не должны утекать в ответы).
    """
    mapper = inspect(model.__class__)
    exclude = set(exclude or [])
    result = {}
    
    for column in mapper.columns:
        if column.name in exclude:
            continue
        value = getattr(model, column.name)
        
        # Обработка специальных типов
        if hasattr(value, 'value'):  # Для Enum
            result[column.name] = value.value
        elif isinstance(value, Decimal):
            result[column.name] = float(value)
        else:
            result[column.name] = value
    
    return result

def models_to_dict(models, exclude: list[str] | None = None):
    items = []
    for model in models:
        items.append(model_to_dict(model=model, exclude=exclude))
    return items
