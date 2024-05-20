from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from typing import Optional

BaseItems = declarative_base()


class FileModel(BaseItems):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True, nullable=True)
    filepath = Column(String, nullable=True)
    item_id = Column(Integer, ForeignKey("items.id"))

    # Связь с элементом (item)
    items = relationship("Item", back_populates="files")


# Модель для региона
class Region(BaseItems):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=True)
    is_active = Column(Boolean(), default=True)

    # Связь с элементами (items)
    items = relationship("Item", back_populates="region")


class QuantitySchool(BaseItems):
    __tablename__ = "quantitys"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=True)
    is_active = Column(Boolean(), default=True)

    # Связь с элементами (items)
    items = relationship("Item", back_populates="quantity")


# Модель для элемента (item)
class Item(BaseItems):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    number_register = Column(String, index=True, nullable=True)
    name_entity = Column(String, index=True, nullable=True)
    tax_name = Column(String, index=True, nullable=True)
    entity_address = Column(String, index=True, nullable=True)
    address_program = Column(String, index=True, nullable=True)
    cipher = Column(String, index=True, nullable=True)
    title_school = Column(String, index=True, nullable=True)
    quantity_school = Column(String, index=True, nullable=True)
    forms_education = Column(String, index=True)
    full_name = Column(String, index=True, nullable=True)
    contract_number = Column(String, index=True, nullable=True)
    issuing_license = Column(String, index=True, nullable=True)
    data_license = Column(String, index=True, nullable=True)
    form_number = Column(String, index=True, nullable=True)
    form_number_suspended = Column(String, index=True, nullable=True)
    form_number_start = Column(String, index=True, nullable=True)
    form_number_stop = Column(String, index=True, nullable=True)
    data_address = Column(String, index=True, nullable=True)
    form_number_data = Column(String, index=True, nullable=True)

    is_active = Column(Boolean(), default=True)

    # Внешний ключ на регион
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=True)
    quantity_id = Column(Integer, ForeignKey("quantitys.id"), nullable=True)

    region = relationship("Region", back_populates="items")
    quantity = relationship("QuantitySchool", back_populates="items")
    files = relationship("FileModel", back_populates="items")
