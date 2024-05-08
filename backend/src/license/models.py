from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from typing import Optional

BaseItems = declarative_base()


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

    full_name = Column(String, index=True, nullable=True)
    contract_number = Column(String, nullable=True)

    is_active = Column(Boolean(), default=True)

    # Внешний ключ на регион
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=True)

    # Связь с регионом
    region = relationship("Region", back_populates="items")
    quantity = relationship("QuantitySchool", back_populates="items")
