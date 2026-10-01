import uuid
from datetime import datetime

from sqlalchemy import UUID, Boolean, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from src.infrastructure.db.models.agent_schema import Agent
from src.infrastructure.db.models.base import Base


class AgentTool(Base):
    __tablename__="agent_tools"

    id: Mapped[uuid.UUID] = mapped_column(
            UUID(
                as_uuid=True
            ),
            primary_key=True,
            default=uuid7
        )

    agent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(
            as_uuid=True
        ),
        ForeignKey(
            "agents.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    agent: Mapped["Agent"] = relationship(
        back_populates="tools"
    )

    tool_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    config: Mapped[dict | None] = mapped_column(
        JSONB(
            none_as_null=True
        ),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(
            timezone=True
        ),
        server_default=func.now()
    )

    __table_args__=(
        UniqueConstraint(
            "agent_id", "tool_name",
            name="uq_agent_tool"
        )
    )
