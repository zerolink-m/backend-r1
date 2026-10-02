# app/routers/config.py
from fastapi import APIRouter, Request
from app.utils import CursedResponser, codes
from config import settings
from app.utils import REGIONS
import logging


router = APIRouter(
    prefix="/v1/config",
    tags=["frontend", "config"]
)

@router.get("")
async def config(request: Request):
    logging.debug(f"config endpoint called, real_ip={request.state.real_ip}")
    return CursedResponser(code=codes.SUCCESS, data={"cursed_version": settings.version, "your-ip": request.state.real_ip})

@router.get("/defaults")
async def defaults():
    logging.debug("defaults endpoint called")
    return CursedResponser(
        code=codes.SUCCESS,
        data=
        {
            "users": {}
        }
    )

@router.get("/regions")
async def regions():
    return CursedResponser(
        code=codes.SUCCESS,
        data=REGIONS
    )