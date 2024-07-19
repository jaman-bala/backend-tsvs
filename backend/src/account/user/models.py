from sqlalchemy import Boolean, Column, String, Enum, JSON, DateTime, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid


BaseUser = declarative_base()


class PortalRole(str, Enum):
    ROLE_PORTAL_USER = "ROLE_PORTAL_USER"
    ROLE_PORTAL_ADMIN = "ROLE_PORTAL_ADMIN"
    ROLE_PORTAL_SUPERADMIN = "ROLE_PORTAL_SUPERADMIN"


class User(BaseUser):

    __tablename__ = "users"

    user_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    avatar = Column(String, nullable=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    birth_year = Column(Date, nullable=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

    is_active = Column(Boolean(), default=True)
    roles = Column(JSON, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def is_superadmin(self) -> bool:
        return PortalRole.ROLE_PORTAL_SUPERADMIN in self.roles

    @property
    def is_admin(self) -> bool:
        return PortalRole.ROLE_PORTAL_ADMIN in self.roles

    def enrich_admin_roles_by_admin_role(self):
        if not self.is_admin:
            return {*self.roles, PortalRole.ROLE_PORTAL_ADMIN}

    def remove_admin_privileges_from_model(self):
        if self.is_admin:
            return {role for role in self.roles if role != PortalRole.ROLE_PORTAL_ADMIN}

