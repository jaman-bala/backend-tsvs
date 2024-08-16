from pydantic import BaseModel
from datetime import datetime


class DepartmentBase(BaseModel):
    title: str
    is_active: bool


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(DepartmentBase):
    pass


class DepartmentSchemas(DepartmentBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class DepartmentOUT(DepartmentBase):
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
