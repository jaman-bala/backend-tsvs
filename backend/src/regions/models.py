from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base


BaseRegion = declarative_base()


#######################
# REGION MODELS
#######################


class Region(BaseRegion):
    """ Модель для региона """

    __tablename__ = "region"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=True)

    is_active = Column(Boolean(), default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связь с элементами (items)
    # items = relationship("ItemLicense", back_populates="region")
