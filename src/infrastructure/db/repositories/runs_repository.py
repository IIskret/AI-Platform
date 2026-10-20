from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import DataBaseExc, RunNotFound
from src.infrastructure.db.models.message_schema import Message
from src.infrastructure.db.models.run_schema import Run, RunStatus
from src.infrastructure.logging.logger import logger


class RunsRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def _flush(self, action: str) -> None:
        try:
            await self._session.flush()
        except SQLAlchemyError as exc:
            logger.exception(f"failed to {action}: {exc}")
            raise DataBaseExc(f"failed to {action}") from exc

    async def create_run(
        self,
        user_id: str,
        agent_id: str,
        run_input: str,
        model: str,
        prompt_version: str,
        tools_version: str,
        idempotency_key: str | None = None,
    ) -> Run:
        run = Run(
            user_id=user_id,
            agent_id=agent_id,
            status=RunStatus.PENDING,
            input=run_input,
            model=model,
            prompt_version=prompt_version,
            tools_version=tools_version,
            idempotency_key=idempotency_key,
        )
        self._session.add(run)
        await self._flush("create run")
        return run

    async def add_message(
        self,
        run_id: UUID,
        role: str,
        content: str | None,
        sequence: int,
    ) -> None:
        self._session.add(
            Message(
                run_id=run_id,
                role=role,
                content=content,
                sequence=sequence,
            )
        )
        await self._flush("add message")

    async def mark_running(self, run_id: UUID) -> None:
        run = await self._session.get(Run, run_id)
        run.status = RunStatus.RUNNING
        run.started_at = datetime.now(UTC)
        await self._flush("mark run running")

    async def complete_run(
        self,
        run_id: UUID,
        output: str,
        input_tokens: int | None,
        output_tokens: int | None,
        latency_ms: int | None,
    ) -> None:
        run = await self._session.get(Run, run_id)
        run.status = RunStatus.COMPLETED
        run.output = output
        run.input_tokens = input_tokens
        run.output_tokens = output_tokens
        run.latency_ms = latency_ms
        run.finished_at = datetime.now(UTC)
        await self._flush("complete run")

    async def fail_run(self, run_id: UUID, error: str) -> None:
        run = await self._session.get(Run, run_id)
        run.status = RunStatus.FAILED
        run.error = error
        run.finished_at = datetime.now(UTC)
        await self._flush("fail run")

    async def get_run(
        self,
        run_id: UUID,
        user_id: str,
    ) -> Run:
        query = select(Run).where(
            Run.id == run_id,
            Run.user_id == user_id,
        )
        run = await self._session.scalar(query)

        if run is None:
            raise RunNotFound("Run not found")

        return run
