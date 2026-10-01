import uuid
from datetime import datetime

from sqlalchemy import UUID, Boolean, DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from src.infrastructure.db.models.agent_tools import AgentTool
from src.infrastructure.db.models.base import Base
from src.infrastructure.db.models.file_schema import File
from src.infrastructure.db.models.run_schema import Run
from src.infrastructure.db.models.user_schema import User


class Agent(Base):
    __tablename__="agents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(
            as_uuid=True
        ),
        primary_key=True,
        default=uuid7
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(
            as_uuid=True
        ),
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        index=True
    )

    user: Mapped["User"] = relationship(
        back_populates="agents"
    )
    runs: Mapped[list["Run"]] = relationship(
        back_populates="agent",
        cascade="all, delete-orphan"
    )
    files: Mapped[list["File"]] = relationship(
        back_populates="agent",
        cascade="all, delete-orphan"
    )
    tools: Mapped[list["AgentTool"]] = relationship(
        back_populates="agent",
        cascade="all, delete-orphan"
    )

    name: Mapped[str] = mapped_column(
        String(128),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    system_prompt: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    model: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    temperature: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    prompt_version: Mapped[str] = mapped_column(
        String(64),
        nullable=False
    )

    tools_version: Mapped[str] = mapped_column(
        String(64),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
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
