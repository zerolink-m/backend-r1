# app/utils/response.py
# aaaaa cursed takoi klassssniy
from app.utils.codes import http_map, detail_map, STREAMING_RESPONSE
from fastapi.responses import JSONResponse, StreamingResponse
from app.utils import detail_map
import json
import logging

def CursedResponser(code: int, data: dict = {}, headers: dict | None = None, error: str | None = None):
    logging.debug(f"CursedResponser called with code={code}, error={error}, headers={headers}")
    return JSONResponse(
        status_code=http_map(code),
        headers=headers,
        content={"code":code, "detail": detail_map(code), "error": error, "data": data}
    )

def CursedJSON(code: int, data: dict, error: str | None = None):
    return {"code": code, "data": data, "detail": detail_map(code), "error": error}

def CursedNDJsonStreamingResponser(generator, code: int = STREAMING_RESPONSE, headers: dict | None = None):
    """
    Потоковый ответ в формате NDJSON: одна строка JSON на каждое событие.
    generator — async-генератор, yield'ящий dict'ы событий.
    Финальная структура каждой строки повторяет формат CursedResponser:
    {"code": ..., "detail": ..., "error": null, "data": {...}}
    """
    logging.debug(f"CursedStreamingResponser called with code={code}")

    async def wrapped():
        async for event in generator:
            yield json.dumps(
                {"code": event.get("code", code), "detail": detail_map(event.get("code", code)), "error": event.get("error"), "data": event.get("data", {})},
                ensure_ascii=False,
                default=str
            ) + "\n"

    base_headers = {
        "X-Code": str(code),
        "Cache-Control": "no-cache",
        #sse?
    }
    if headers:
        base_headers.update(headers)

    return StreamingResponse(
        wrapped(),
        status_code=http_map(code),
        media_type="application/x-ndjson",
        headers=base_headers
    )

def CursedStreamingResponser(generator, media_type: str = "application/octet-stream", code: int = STREAMING_RESPONSE, headers: dict | None = None):
    """
    Потоковый ответ в бинарном формате.
    generator — async-генератор, yield'ящий события.
    """
    logging.debug(f"CursedStreamingResponser called with code={code}")

    async def wrapped():
        async for event in generator:
            yield event

    base_headers = {
        "X-Code": str(code),
        "Cache-Control": "no-cache",
        #sse?
    }
    if headers:
        base_headers.update(headers)

    return StreamingResponse(
        wrapped(),
        status_code=http_map(code),
        media_type=media_type,
        headers=base_headers
    )

class CursedException(Exception):
    def __init__(self, code: int, error: str = None):
        logging.debug(f"CursedException raised with code={code}, error={error}")
        self.code = code
        self.error = error or None
        self.details = detail_map(code)
