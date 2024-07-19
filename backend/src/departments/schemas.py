from pydantic import BaseModel
from typing import List, Optional


class DepartmentBase(BaseModel):
    title: str


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(DepartmentBase):
    pass


class DepartmentSchemas(DepartmentBase):
    id: int
    is_active: bool
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        orm_mode = True


class DepartmentOUT(DepartmentBase):
    id: int
    title: str

    class Config:
        orm_mode = True
