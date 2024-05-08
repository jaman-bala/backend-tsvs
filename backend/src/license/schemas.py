from pydantic import BaseModel
from typing import Optional


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class ShowRegionBase(TunedModel):
    id: int
    name: str
    is_active: bool


class RegionOUT(ShowRegionBase):
    id: int
    name: str
    is_active: Optional[bool]


class RegionCreate(BaseModel):
    name: str


class ShowItemBase(TunedModel):
    id: int
    name: str
    full_name: str
    contract_number: str
    is_active: bool


class ItemOUT(ShowItemBase):
    id: int
    full_name: str
    contract_number: str
    region_id: int
    is_active: Optional[bool]


class ItemCreate(BaseModel):
    name: str
    full_name: str
    contract_number: str
    region_id: int



