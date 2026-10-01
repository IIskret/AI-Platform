import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from src.infrastructure.db.models.base import Base
from src.infrastructure.db.models.run_schema import Run


class Message(Base):
    __tablename__="messages"

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
        back_populates="messages"
    )

    role: Mapped[str] = mapped_column(
        String(20)
    )

    content: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    sequence: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(
            timezone=True
        ),
        server_default=func.now()
    )

    __table_args__= (
        Index(
            "ix_messages_run_id_sequence",
            "run_id",
            "sequence"
        )
    )
