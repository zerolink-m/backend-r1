# app/utils/logger.py - логер крч

import logging
import sys
from logging.handlers import RotatingFileHandler

from config import settings, LoggingEnum

def setup_logging() -> None:
    root = logging.getLogger()
    root.setLevel(settings.log_level.value)

    root.handlers.clear()
    fmt = logging.Formatter(settings.log_format, datefmt=settings.log_date_format)

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(fmt)
    root.addHandler(console)
    if settings.log_file_enabled:
        file_handler = RotatingFileHandler(
            settings.log_file,
            maxBytes=settings.log_file_max_size * 1024 * 1024,
            backupCount=settings.log_file_backup_count,
            encoding="utf-8"
        )
        file_handler.setFormatter(fmt)
        root.addHandler(file_handler)

    for name in ("uvicorn", "uvicorn.access", "uvicorn.error"):
        lg = logging.getLogger(name)
        lg.handlers.clear()
        lg.propagate = True

    # sqlalchemy шумит на инфо
    if settings.log_level != LoggingEnum.DEBUG:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    root.debug(f"Logging configured: level={settings.log_level.value}, file_enabled={settings.log_file_enabled}")

