from pydantic import BaseModel
from datetime import datetime


# Схема для регионов
class RegionBase(BaseModel):
    title: str
    is_active: bool


class RegionCreate(RegionBase):
    pass


class RegionUpdate(RegionBase):
    pass


class RegionSchemas(RegionBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class RegionOUT(RegionBase):
    id: int
    title: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Is_activeShemasOUT(BaseModel):
    is_active: bool
    updated_at: datetime

    class Config:
        orm_mode = True
