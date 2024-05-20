from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

#######################
# FILE SCHEMAS
#######################


class FileCreate(BaseModel):
    filename: str
    filepath: str


class FileOUT(BaseModel):
    id: int
    filename: str
    filepath: str

    class Config:
        from_attributes = True


#######################
# REGION SCHEMAS
#######################


class TunedModel(BaseModel):
    class Config:
        from_attributes = True


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


#######################
# QuantitySchool SCHEMAS
#######################

class ShowQuantitySchoolBase(TunedModel):
    id: int
    name: str
    is_active: bool


class QuantitySchoolOUT(ShowRegionBase):
    id: int
    name: str
    is_active: Optional[bool]


class QuantitySchoolCreate(BaseModel):
    name: str


#######################
# ITEM SCHEMAS
#######################

class ShowItemBase(TunedModel):
    id: int
    number_register: str
    name_entity: str
    tax_name: str
    entity_address: str
    address_program: str
    cipher: str
    title_school: str
    quantity_school: str
    forms_education: str
    full_name: str
    contract_number: str
    issuing_license: str
    data_license: datetime
    form_number: str
    form_number_suspended: str
    form_number_start: str
    form_number_stop: str
    data_address: str
    form_number_data: str

    is_active: bool


class ItemSchemasOUT(ShowItemBase):
    id: int
    number_register: str
    name_entity: str
    tax_name: str
    entity_address: str
    address_program: str
    cipher: str
    title_school: str
    quantity_school: str
    forms_education: str
    full_name: str
    contract_number: str
    issuing_license: str
    data_license: str
    form_number: str
    form_number_suspended: str
    form_number_start: str
    form_number_stop: str
    data_address: str
    form_number_data: str
    region_id: int
    quantity_id: int

    is_active: Optional[bool]
    files: List[FileOUT]


class ItemCreate(BaseModel):
    number_register: str
    name_entity: str
    tax_name: str
    entity_address: str
    address_program: str
    cipher: str
    title_school: str
    quantity_school: str
    forms_education: str
    full_name: str
    contract_number: str
    issuing_license: str
    data_license: str
    form_number: str
    form_number_suspended: str
    form_number_start: str
    form_number_stop: str
    data_address: str
    form_number_data: str
    region_id: int
    quantity_id: int
