# app/routers/__init__.py

from .config import router as config_router
from .middleware import CursedMiddleware
from .users import router as users_router
from .datacenters import router as datacenters_router
from .lifespan import lifespan

__all__ = [
    # Routers
    "config_router",
    "users_router",
    "datacenters_router",
    "tariffs_router",
    # Middleware
    "CursedMiddleware",
    "lifespan"
]
