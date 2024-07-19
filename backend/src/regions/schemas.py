from pydantic import BaseModel
from typing import List, Optional


# Схема для регионов
class RegionBase(BaseModel):
    title: str


class RegionCreate(RegionBase):
    pass


class RegionUpdate(RegionBase):
    pass


class RegionSchemas(RegionBase):
    id: int
    is_active: bool
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        orm_mode = True


class RegionOUT(RegionBase):
    id: int
    title: str

    class Config:
        orm_mode = True
