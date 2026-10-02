# app/models/datacenters.py
'''
CREATE TABLE datacenters (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    location VARCHAR(128) NOT NULL DEFAULT 'Unknown location server',
    country VARCHAR(16) NOT NULL DEFAULT 'Unknown country server',
    city VARCHAR(18) NOT NULL DEFAULT 'Unknown city server',
    guaranted_radius INTEGER NOT NULL DEFAULT '1000',
    speed_type ENUM(DatacenterSpeedType) NOT NULL DEFAULT 'up_to_mbits',
    speed INTEGER NOT NULL DEFAULT '10',
    status_url VARCHAR(255) NOT NULL DEFAULT 'https://status.qpda.ru/status/zl',
    status ENUM(DatacenterStatus) NOT NULL DEFAULT 'operational',
    is_available BOOL NOT NULL DEFAULT true,
    remnawave_supported BOOL NOT NULL DEFAULT false,
    remnawave_url VARCHAR(128) NULL,
    remnawave_token VARCHAR(255) NULL,
    remnawave_internal_squad VARCHAR(32) NULL,
    amnezia_supported BOOL NOT NULL DEFAULT false,
    wireguard_supported BOOL NOT NULL DEFAULT false,
    wgdashboard_url VARCHAR(128) NULL,
    wgdashboard_token VARCHAR(255) NULL,
    wireguard_interface VARCHAR(16) NULL,
    amnezia_interface VARCHAR(16) NULL,
    updated_at BIGINT NOT NULL,
    added_at BIGINT NOT NULL
)
'''

from enum import Enum

from sqlalchemy import Enum as SAEnum, String, Integer, Boolean, true, false, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class DatacenterSpeedType(str, Enum):
    up_to_mbits = "up_to_mbits"
    up_to_gbits = "up_to_gbits"


class DatacenterStatus(str, Enum):
    operational = "operational"
    degraded = "degraded"
    down = "down"
    maintenance = "maintenance"


class Datacenter(Base):
    __tablename__ = "datacenters"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    location: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        server_default="Unknown location server"
    )

    country: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        server_default="Unknown country server"
    )

    city: Mapped[str] = mapped_column(
        String(18),
        nullable=False,
        server_default="Unknown city server"
    )

    guaranted_radius: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="1000"
    )

    speed_type: Mapped[DatacenterSpeedType] = mapped_column(
        SAEnum(DatacenterSpeedType),
        nullable=False,
        server_default="up_to_mbits"
    )

    speed: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="10"
    )

    status_url: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        server_default="https://status.qpda.ru/status/zl"
    )

    status: Mapped[DatacenterStatus] = mapped_column(
        SAEnum(DatacenterStatus),
        nullable=False,
        server_default="operational"
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=true()
    )

    remnawave_supported: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=false()
    )

    remnawave_url: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True
    )

    remnawave_token: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    remnawave_internal_squad: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True
    )

    amnezia_supported: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=false()
    )

    wireguard_supported: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=false()
    )

    wgdashboard_url: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True
    )

    wgdashboard_token: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    wireguard_interface: Mapped[str | None] = mapped_column(
        String(16),
        nullable=True
    )

    amnezia_interface: Mapped[str | None] = mapped_column(
        String(16),
        nullable=True
    )

    updated_at: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    added_at: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )
