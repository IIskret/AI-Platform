import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BIGINT, UUID, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from src.infrastructure.db.models.base import Base

if TYPE_CHECKING:
    from src.infrastructure.db.models.agent_schema import Agent
    from src.infrastructure.db.models.user_schema import User


class File(Base):
    __tablename__="files"


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

    agent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(
            as_uuid=True
        ),
        ForeignKey(
            "agents.id",
            ondelete="CASCADE"
        ),
        nullable=True,
        index=True
    )

    user: Mapped["User"] = relationship(
        back_populates="files"
    )
    agent: Mapped["Agent | None"] = relationship(
        back_populates="files"
    )

    filename: Mapped[str] = mapped_column(
        String(512),
        nullable=False
    )

    storage_key: Mapped[str] = mapped_column(
        String(512),
        nullable=False
    )

    mime_type: Mapped[str] = mapped_column(
        String(127),
        nullable=False
    )

    size_bytes: Mapped[int] = mapped_column(
        BIGINT,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(
            timezone=True
        ),
        server_default=func.now()
    )
