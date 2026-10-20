from uuid import UUID

from fastapi import HTTPException, status

from src.core.exceptions import AgentNotFound, RunNotFound
from src.dto.agent.agent_output import AgentOutput
from src.dto.runs.create_run import CreateRun
from src.dto.runs.run_output import RunOutput
from src.infrastructure.db.models.run_schema import Run
from src.infrastructure.db.repositories.agent_repository import AgentRepository
from src.infrastructure.db.repositories.runs_repository import RunsRepository
from src.infrastructure.llm.mistral import MistralProvider
from src.infrastructure.logging.logger import logger


class RunsService:
    def __init__(
        self,
        runs_repository: RunsRepository,
        agent_repository: AgentRepository,
        llm_provider: MistralProvider,
        user_id: str,
    ) -> None:
        self._runs_repository: RunsRepository = runs_repository
        self._agent_repository: AgentRepository = agent_repository
        self._llm_provider: MistralProvider = llm_provider
        self._user_id: str = user_id

    async def create_run(self, agent_id: UUID, schema: CreateRun) -> RunOutput:
        agent = await self._get_agent(agent_id)

        run = await self._runs_repository.create_run(
            user_id=self._user_id,
            agent_id=str(agent_id),
            run_input=schema.input,
            model=agent.model,
            prompt_version="v1",
            tools_version="v1",
        )

        await self._runs_repository.add_message(
            run_id=run.id,
            role="user",
            content=schema.input,
            sequence=1,
        )
        await self._runs_repository.mark_running(run.id)

        try:
            result = await self._llm_provider.complete(
                messages=self._build_messages(agent, schema.input),
                model=agent.model,
            )
        except Exception as exc:
            logger.exception(f"run {run.id} failed: {exc}")
            await self._runs_repository.fail_run(run.id, error=str(exc)[:2000])
            return self._to_output(run)

        await self._runs_repository.add_message(
            run_id=run.id,
            role="assistant",
            content=result.content,
            sequence=2,
        )
        await self._runs_repository.complete_run(
            run_id=run.id,
            output=result.content,
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            latency_ms=result.latency_ms,
        )
        return self._to_output(run)

    async def get_run(self, run_id: UUID) -> RunOutput:
        try:
            run = await self._runs_repository.get_run(
                run_id=run_id,
                user_id=self._user_id,
            )
        except RunNotFound as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Run not found",
            ) from exc

        return self._to_output(run)

    async def _get_agent(self, agent_id: UUID) -> AgentOutput:
        try:
            return await self._agent_repository.get_agent_by_id(
                agent_id=str(agent_id),
                user_id=self._user_id,
            )
        except AgentNotFound as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found",
            ) from exc

    @staticmethod
    def _build_messages(agent: AgentOutput, user_input: str) -> list[dict]:
        messages: list[dict] = []
        if agent.system_prompt:
            messages.append({"role": "system", "content": agent.system_prompt})
        messages.append({"role": "user", "content": user_input})
        return messages

    @staticmethod
    def _to_output(run: Run) -> RunOutput:
        return RunOutput(
            run_id=run.id,
            agent_id=run.agent_id,
            status=run.status,
            input=run.input,
            output=run.output,
            error=run.error,
            model=run.model,
            prompt_version=run.prompt_version,
            tools_version=run.tools_version,
            input_tokens=run.input_tokens,
            output_tokens=run.output_tokens,
            latency_ms=run.latency_ms,
        )
