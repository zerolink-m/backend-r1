# app/models/subscriptions.py
'''
CREATE TABLE subscriptions (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    datacenter_id INTEGER NOT NULL,
    manual_enabled BOOL NOT NULL DEFAULT false,
    enabled BOOL NOT NULL DEFAULT true,
    method_one ENUM(MethodOne) NOT NULL DEFAULT 'none',
    method_two ENUM(MethodTwo) NOT NULL DEFAULT 'none',
    traffic BIGINT NOT NULL DEFAULT '0',
    unlimited BOOL NOT NULL DEFAULT false,
    unlimited_until BIGINT NULL,
    used_traffic BIGINT NOT NULL DEFAULT '0',
    used_traffic_snapshot BIGINT NOT NULL DEFAULT '0',
    used_traffic_wgdashboard BIGINT NOT NULL DEFAULT '0',
    used_traffic_remnawave BIGINT NOT NULL DEFAULT '0',
    used_traffic_del BIGINT NOT NULL DEFAULT '0',
    used_traffic_add BIGINT NOT NULL DEFAULT '0',
    wgdashboard_public_key VARCHAR(255) NULL,
    wgdashboard_config VARCHAR(128) NULL,
    remnawave_id BIGINT NULL,
    remnawave_sub_url VARCHAR(128) NULL,
    last_ip_remnawave VARCHAR(64) NULL,
    last_ip_wgdashboard VARCHAR(64) NULL,
    last_port_remnawave INTEGER NULL,
    last_port_wgdashboard INTEGER NULL,
    last_seen_at_remnawave BIGINT NULL,
    last_seen_at_wgdashboard BIGINT NULL,
    updated_at BIGINT NOT NULL,
    added_at BIGINT NOT NULL
)

CREATE TABLE subscriptions_stats_hours (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    subscription_id INTEGER NOT NULL,
    datacenter_id INTEGER NOT NULL,
    method_one ENUM(MethodOne) NOT NULL DEFAULT 'none',
    method_two ENUM(MethodTwo) NOT NULL DEFAULT 'none',
    unlimited BOOL NOT NULL DEFAULT false,
    used_traffic_wgdashboard BIGINT NULL,
    used_traffic_remnawave BIGINT NULL,
    ip_remnawave VARCHAR(64) NULL,
    ip_wgdashboard VARCHAR(64) NULL,
    port_remnawave INTEGER NULL,
    port_wgdashboard INTEGER NULL,
    seen_at_remnawave BIGINT NULL,
    seen_at_wgdashboard BIGINT NULL,
    hour_at INTEGER NOT NULL,
    day_at INTEGER NOT NULL,
    added_at BIGINT NOT NULL
)

CREATE TABLE subscriptions_stats_months (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    subscription_id INTEGER NOT NULL,
    unlimited BOOL NOT NULL DEFAULT false,
    used_traffic_wgdashboard BIGINT NULL,
    used_traffic_remnawave BIGINT NULL,
    ip_remnawave VARCHAR(64) NULL,
    ip_wgdashboard VARCHAR(64) NULL,
    month_at BIGINT NOT NULL,
    added_at BIGINT NOT NULL
)

CREATE TABLE subscriptions_events (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    action ENUM(SubscriptionEventAction) NOT NULL,
    subscription_id INTEGER NOT NULL,
    packet_id BIGINT NULL,
    datacenter_id INTEGER NULL,
    method_one ENUM(MethodOne) NULL DEFAULT 'none',
    method_two ENUM(MethodTwo) NULL DEFAULT 'none',
    unlimited BOOL NULL DEFAULT false,
    unlimited_until BIGINT NULL,
    added_by BIGINT NULL,
    added_at BIGINT NOT NULL
)
'''

from enum import Enum

from sqlalchemy import BigInteger, Enum as SAEnum, String, Integer, Boolean, true, false
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class MethodOne(str, Enum):
    amnezia = "amnezia"
    wireguard = "wireguard"
    none = "none"

class MethodTwo(str, Enum):
    remnawave = "remnawave"
    none = "none"

class SubscriptionEventAction(str, Enum):
    created = "created"
    enabled = "enabled"
    disabled = "disabled"
    datacenter_changed = "datacenter_changed"
    protocol_one_changed = "protocol_one_changed"
    protocol_two_changed = "protocol_two_changed"
    unlimited_expired = "unlimited_expired"
    unlimited_buyed = "unlimited_buyed"
    traffic_buyed = "traffic_buyed"


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    datacenter_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    manual_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=false()
    )

    enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=true()
    )

    method_one: Mapped[MethodOne] = mapped_column(
        SAEnum(MethodOne),
        nullable=False,
        server_default="none"
    )

    method_two: Mapped[MethodTwo] = mapped_column(
        SAEnum(MethodTwo),
        nullable=False,
        server_default="none"
    )

    traffic: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default="0"
    )

    unlimited: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=false()
    )

    unlimited_until: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    used_traffic: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default="0"
    )

    used_traffic_snapshot: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default="0"
    )

    used_traffic_wgdashboard: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default="0"
    )

    used_traffic_remnawave: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default="0"
    )

    used_traffic_del: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default="0"
    )

    used_traffic_add: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default="0"
    )

    wgdashboard_public_key: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    wgdashboard_config: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True
    )

    remnawave_id: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    remnawave_sub_url: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True
    )

    last_ip_remnawave: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    last_ip_wgdashboard: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    last_port_remnawave: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    last_port_wgdashboard: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    last_seen_at_remnawave: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
    )

    last_seen_at_wgdashboard: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
    )

    updated_at: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    added_at: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

class SubscriptionStatHour(Base):
    __tablename__ = "subscriptions_stats_hours"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    subscription_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    datacenter_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    method_one: Mapped[MethodOne] = mapped_column(
        SAEnum(MethodOne),
        nullable=False,
        server_default="none"
    )

    method_two: Mapped[MethodTwo] = mapped_column(
        SAEnum(MethodTwo),
        nullable=False,
        server_default="none"
    )

    unlimited: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=false()
    )

    used_traffic_wgdashboard: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    used_traffic_remnawave: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    ip_remnawave: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    ip_wgdashboard: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True
    )

    port_remnawave: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    port_wgdashboard: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    seen_at_remnawave: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    seen_at_wgdashboard: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    hour_at: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    day_at: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    added_at: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

class SubscriptionStatMonth(Base):
    __tablename__ = "subscriptions_stats_months"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    subscription_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    unlimited: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=false()
    )

    used_traffic_wgdashboard: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    used_traffic_remnawave: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    ip_remnawave: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    ip_wgdashboard: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True
    )

    month_at: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    added_at: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

class SubscriptionEvent(Base):
    __tablename__ = "subscriptions_events"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    action: Mapped[SubscriptionEventAction] = mapped_column(
        SAEnum(SubscriptionEventAction),
        nullable=False
    )

    subscription_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    packet_id: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    datacenter_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    method_one: Mapped[MethodOne | None] = mapped_column(
        SAEnum(MethodOne),
        nullable=True,
        server_default="none"
    )

    method_two: Mapped[MethodTwo | None] = mapped_column(
        SAEnum(MethodTwo),
        nullable=True,
        server_default="none"
    )

    unlimited: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
        server_default=false()
    )

    unlimited_until: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    added_by: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    added_at: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )