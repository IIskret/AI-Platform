import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import UUID, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from src.infrastructure.db.models.base import Base

if TYPE_CHECKING:
    from src.infrastructure.db.models.run_schema import Run


class ToolCall(Base):
    __tablename__="tool_calls"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid7
    )

    run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(
            as_uuid=True
        ),
        ForeignKey(
            "runs.id",
            ondelete="CASCADE"
        ),
        index=True
    )

    run: Mapped["Run"] = relationship(
        back_populates="tools"
    )

    tool_name: Mapped[str] = mapped_column(
        String(128),
        nullable=False
    )

    arguments: Mapped[dict | None] = mapped_column(
        JSONB(
            none_as_null=True
        ),
        nullable=True
    )

    result: Mapped[dict | None] = mapped_column(
        JSONB(
            none_as_null=True
        ),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    duration_ms: Mapped[int] = mapped_column(
        Integer,
        nullable=False
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
