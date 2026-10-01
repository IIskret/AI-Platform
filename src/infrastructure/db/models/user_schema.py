import enum
import uuid
from datetime import datetime

from sqlalchemy import UUID, Boolean, DateTime, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from src.infrastructure.db.models.agent_schema import Agent
from src.infrastructure.db.models.base import Base
from src.infrastructure.db.models.file_schema import File
from src.infrastructure.db.models.run_schema import Run


class UserRole(str, enum.StrEnum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__="users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid7
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean(),
        default=True
    )

    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole),
        default=UserRole.USER,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(
            timezone=True
        ),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(
            timezone=True
        ),
        server_default=func.now(),
        onupdate=func.now()
    )

    agents: Mapped[list["Agent"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    runs: Mapped[list["Run"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    files: Mapped[list["File"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

