from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

BaseItems = declarative_base()


# Модель для региона
class Region(BaseItems):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    is_active = Column(Boolean(), default=True)

    # Связь с элементами (items)
    items = relationship("Item", back_populates="region")


# Модель для элемента (item)
class Item(BaseItems):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    full_name = Column(String, index=True)
    contract_number = Column(String)
    is_active = Column(Boolean(), default=True)

    # Внешний ключ на регион
    region_id = Column(Integer, ForeignKey("regions.id"))

    # Связь с регионом
    region = relationship("Region", back_populates="items")
