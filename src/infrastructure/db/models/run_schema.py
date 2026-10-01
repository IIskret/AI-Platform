import enum
import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from src.infrastructure.db.models.agent_schema import Agent
from src.infrastructure.db.models.base import Base
from src.infrastructure.db.models.message_schema import Message
from src.infrastructure.db.models.tool_call_schema import ToolCall
from src.infrastructure.db.models.user_schema import User


class RunStatus(str, enum.StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class Run(Base):
    __tablename__="runs"

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
        ),
        index=True
    )

    agent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(
            as_uuid=True
        ),
        ForeignKey(
            "agents.id",
            ondelete="CASCADE"
        ),
        index=True
    )

    user: Mapped["User"] = relationship(
        back_populates="runs"
    )
    agent: Mapped["Agent"] = relationship(
        back_populates="runs"
    )
    messages: Mapped[list["Message"]] = relationship(
        back_populates="run",
        cascade="all, delete-orphan"
    )
    tools: Mapped[list["ToolCall"]] = relationship(
        back_populates="run",
        cascade="all, delete-orphan"
    )


    status: Mapped[RunStatus] = mapped_column(
        SQLEnum(RunStatus),
        nullable=False
    )

    input: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    output: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    idempotency_key: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
        index=True
    )

    model: Mapped[str] = mapped_column(
        String(128),
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

    input_tokens: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    output_tokens: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    latency_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(
            timezone=True
        ),
        nullable=True
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(
            timezone=True
        ),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(
            timezone=True
        ),
        server_default=func.now()
    )
