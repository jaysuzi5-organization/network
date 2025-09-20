"""
Network Model and Pydantic Schema

This module defines:
- The SQLAlchemy ORM model for persisting Network data.
- The Pydantic schema for validating API requests when creating a Network.
"""

from sqlalchemy import Column, DateTime, Integer, String, Boolean, Float
from framework.db import Base
from datetime import datetime, UTC
from pydantic import BaseModel
from typing import Optional


class Network(Base):
    """
    SQLAlchemy ORM model representing a Network record.
    """

    __tablename__ = "network"

    id = Column(Integer, primary_key=True, index=True)

    # Uptime
    uptime_days = Column(Integer, nullable=False, default=0)
    uptime_hours = Column(Integer, nullable=False, default=0)
    uptime_minutes = Column(Integer, nullable=False, default=0)

    # Status
    led_status = Column(String(50), nullable=False)
    online = Column(Boolean, nullable=False, default=False)
    ethernet_link = Column(Boolean, nullable=False, default=False)
    update_required = Column(Boolean, nullable=False, default=False)

    # Networking
    ip_method = Column(String(20), nullable=False)  # e.g. DHCP / STATIC
    ip_address = Column(String(45), nullable=False)  # IPv4/IPv6
    gateway = Column(String(45), nullable=False)
    local_ip_address = Column(String(45), nullable=False)
    dns_servers = Column(String(200), nullable=True)
    dns = Column(String(200), nullable=True)

    # Lease info
    lease_days = Column(Integer, nullable=False, default=0)
    lease_hours = Column(Integer, nullable=False, default=0)
    lease_minutes = Column(Integer, nullable=False, default=0)

    # Metrics
    tcp_latency = Column(Float, nullable=True)
    internet_download = Column(Float, nullable=True)
    internet_upload = Column(Float, nullable=True)
    internet_ping = Column(Float, nullable=True)

    # Timestamps
    create_date = Column(DateTime, default=lambda: datetime.now(UTC))
    update_date = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC)
    )

    def __repr__(self):
        return f"<Network(id={self.id}, ip='{self.ip_address}', online={self.online})>"


class NetworkCreate(BaseModel):
    """
    Pydantic schema for creating a new Network record.
    """
    uptime_days: int
    uptime_hours: int
    uptime_minutes: int
    led_status: str
    online: bool
    ip_method: str
    ip_address: str
    gateway: str
    local_ip_address: str
    lease_days: int
    lease_hours: int
    lease_minutes: int
    dns_servers: Optional[str] = None
    ethernet_link: bool
    update_required: bool
    dns: Optional[str] = None
    tcp_latency: Optional[float] = None
    internet_download: Optional[float] = None
    internet_upload: Optional[float] = None
    internet_ping: Optional[float] = None
