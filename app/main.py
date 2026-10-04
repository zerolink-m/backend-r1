from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.utils import http_map #, CursedResponser
from app.utils.response import CursedException
from app.routers import config, middleware, users, lifespan
from config import settings
import logging

app = FastAPI(
    title="ZeroLink VPN API",
    lifespan=lifespan,
    description="Powerful service for vpn ex: wireguard, amnezia (wireguardDashboard) or vless (remnawave)",
    version=settings.version,
    root_path="/cursedapi/zerolink",
    servers=[{"url":"https://zerolink.ru.net"}],
    terms_of_service="https://zerolink.ru.net/terms",
    contact={"name": "Support", "email": "zlsup@zerolink.ru.net"}
)

@app.exception_handler(CursedException)
async def cursed_exception_handler(request: Request, exc: CursedException):
    logging.debug(f"cursed_exception_handler: code={exc.code}, error={exc.error}, path={request.url.path}")
    return JSONResponse(
        status_code=http_map(exc.code),
        content={"code": exc.code, "details": exc.details, "error": exc.error, "data": {}},
    )

app.add_middleware(middleware.CursedMiddleware)
app.include_router(config.router)
app.include_router(users.router)
