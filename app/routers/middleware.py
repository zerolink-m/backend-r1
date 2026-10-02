# app/routers/middleware.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from config import settings, TrustIpMethodEnum
import logging


class CursedMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # До
        # Реализация траст айпи

        ip = request.client.host if request.client else None

        x_real_ip = request.headers.get("x-real-ip")
        proxy_pass = request.headers.get("proxy-pass-ip")

        logging.debug(f"CursedMiddleware.dispatch: ip={ip}, x_real_ip={x_real_ip}, proxy_pass={proxy_pass}, trust_ip_method={settings.trust_ip_method}")

        # Проверка если айпи
        if settings.trust_ip_method == TrustIpMethodEnum.IP:
            if ip == settings.trust_ip_value:
                request.state.real_ip = x_real_ip or ip
            else:
                request.state.real_ip = ip

        # Проверка если строка
        elif settings.trust_ip_method == TrustIpMethodEnum.STRING:
            if proxy_pass == settings.trust_ip_value:
                request.state.real_ip = x_real_ip or ip
            else:
                request.state.real_ip = ip

        # Иначе
        else: # TrustIpMethodEnum.NO
            request.state.real_ip = ip

        logging.debug(f"CursedMiddleware.dispatch: resolved real_ip={request.state.real_ip}")

        response =  await call_next(request)
        # После
        return response
