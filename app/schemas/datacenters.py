# app/schemas/datacenters.py
from app.schemas import DataBaseModel
from typing import Optional
from pydantic import Field, AnyHttpUrl
from app.models.datacenters import DatacenterSpeedType, DatacenterStatus


class EditDatacenter(DataBaseModel):
    location: Optional[str] = Field(default=None, max_length=128)
    country: Optional[str] = Field(default=None, max_length=16)
    city: Optional[str] = Field(default=None, max_length=18)
    guaranted_radius: Optional[int] = Field(default=None)
    speed_type: Optional[DatacenterSpeedType] = Field(default=None)
    speed: Optional[int] = Field(default=None)
    status_url: Optional[AnyHttpUrl] = None
    status: Optional[DatacenterStatus] = Field(default=None)
    is_available: Optional[bool] = Field(default=None)
    remnawave_supported: Optional[bool] = Field(default=None)
    remnawave_url: Optional[AnyHttpUrl] = None
    remnawave_token: Optional[str] = Field(default=None, max_length=255)
    remnawave_internal_squad: Optional[str] = Field(default=None, max_length=32)
    amnezia_supported: Optional[bool] = Field(default=None)
    wireguard_supported: Optional[bool] = Field(default=None)
    wgdashboard_url: Optional[AnyHttpUrl] = None
    wgdashboard_token: Optional[str] = Field(default=None, max_length=255)
    wireguard_interface: Optional[str] = Field(default=None, max_length=16)
    amnezia_interface: Optional[str] = Field(default=None, max_length=16)
    updated_at: Optional[int] = Field(default=None, ge=1, le=9223372036854775807)
    added_at: Optional[int] = Field(default=None, ge=1, le=9223372036854775807)
    migrate_subscriptions: Optional[bool] = Field(default=None)


class CreateDatacenter(DataBaseModel):
    location: str = Field(default="Unknown location server", max_length=128)
    country: str = Field(default="Unknown country server", max_length=16)
    city: str = Field(default="Unknown city server", max_length=18)
    guaranted_radius: int = Field(default=1000)
    speed_type: DatacenterSpeedType = Field(default=DatacenterSpeedType.up_to_mbits)
    speed: int = Field(default=10)
    status_url: AnyHttpUrl = None
    status: DatacenterStatus = Field(default=DatacenterStatus.operational)
    is_available: bool = Field(default=True)
    remnawave_supported: bool = Field(default=False)
    remnawave_url: Optional[AnyHttpUrl] = None
    remnawave_token: Optional[str] = Field(default=None, max_length=255)
    remnawave_internal_squad: Optional[str] = Field(default=None, max_length=32)
    amnezia_supported: bool = Field(default=False)
    wireguard_supported: bool = Field(default=False)
    wgdashboard_url: Optional[AnyHttpUrl] = None
    wgdashboard_token: Optional[str] = Field(default=None, max_length=255)
    wireguard_interface: Optional[str] = Field(default=None, max_length=16)
    amnezia_interface: Optional[str] = Field(default=None, max_length=16)