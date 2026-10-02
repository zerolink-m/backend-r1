#!/usr/bin/python3
import uvicorn

# Импорт и настройка логов до app
from app.utils.logger import setup_logging
setup_logging()

from config import settings
from app.main import app

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
