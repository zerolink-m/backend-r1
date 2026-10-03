# app/schemas/datacenters.py
from app.schemas import DataBaseModel
from typing import Optional
from pydantic import Field
from app.models.datacenters import DatacenterSpeedType, DatacenterStatus


class EditDatacenter(DataBaseModel):
    location: Optional[str] = Field(default=None, max_length=128)
    country: Optional[str] = Field(default=None, max_length=16)
    city: Optional[str] = Field(default=None, max_length=18)
    guaranted_radius: Optional[int] = Field(default=None)
    speed_type: Optional[DatacenterSpeedType] = Field(default=None)
    speed: Optional[int] = Field(default=None)
    status_url: Optional[str] = Field(default=None, max_length=255)
    status: Optional[DatacenterStatus] = Field(default=None)
    is_available: Optional[bool] = Field(default=None)
    remnawave_supported: Optional[bool] = Field(default=None)
    remnawave_url: Optional[str] = Field(default=None, max_length=128)
    remnawave_token: Optional[str] = Field(default=None, max_length=255)
    remnawave_internal_squad: Optional[str] = Field(default=None, max_length=32)
    amnezia_supported: Optional[bool] = Field(default=None)
    wireguard_supported: Optional[bool] = Field(default=None)
    wgdashboard_url: Optional[str] = Field(default=None, max_length=128)
    wgdashboard_token: Optional[str] = Field(default=None, max_length=255)
    wireguard_interface: Optional[str] = Field(default=None, max_length=16)
    amnezia_interface: Optional[str] = Field(default=None, max_length=16)
    updated_at: Optional[int] = Field(default=None, ge=1, le=9223372036854775807)
    added_at: Optional[int] = Field(default=None, ge=1, le=9223372036854775807)