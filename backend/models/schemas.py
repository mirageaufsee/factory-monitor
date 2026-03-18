from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DeviceCreate(BaseModel):
    name: str
    location: str
    device_type: str


class DeviceResponse(BaseModel):
    id: int
    name: str
    location: str
    device_type: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class SensorDataCreate(BaseModel):
    device_id: int
    temperature: float
    pressure: float
    rpm: float


class SensorDataResponse(BaseModel):
    id: int
    device_id: int
    temperature: float
    pressure: float
    rpm: float
    timestamp: datetime

    class Config:
        from_attributes = True


class AlertResponse(BaseModel):
    id: int
    device_id: int
    message: str
    severity: str
    resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True