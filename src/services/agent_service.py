from src.dto.agent.agent_output import AgentOutput
from src.dto.agent.create_agent import CreateAgent
from src.dto.agent.update_agent import UpdateAgent
from src.infrastructure.db.repositories.agent_repository import AgentRepository


class AgentService:
    def __init__(
        self, 
        agent_repository: AgentRepository, 
        user_id: str 
    ) -> None:
        self._agent_repository: AgentRepository = agent_repository
        self._user_id: str = user_id

    async def create_agent(self, schema: CreateAgent) -> AgentOutput | None:
        return await self._agent_repository.create(
            user_id=self._user_id,
            
            name=schema.name,
            description=schema.description,
            system_prompt=schema.system_prompt,
            model=schema.model,
            temperature=schema.temperature
        )

    async def get_user_agents(self) -> list[AgentOutput]:
        return await self._agent_repository.get_agents(
            user_id=self._user_id
        )

    async def agent_by_id(self, agent_id: str) -> AgentOutput | None:
        return await self._agent_repository.get_agent_by_id(
            agent_id=agent_id,
            user_id=self._user_id
        )

    async def update_user_agent(self, agent_id: str, schema: UpdateAgent) -> AgentOutput:
        return await self._agent_repository.update_agent(
            user_id=self._user_id,
            agent_id=agent_id,
            schema=schema
        )

    async def delete_user_agent(self, agent_id: str) -> None:
        return await self._agent_repository.delete_agent(
            user_id=self._user_id,
            agent_id=agent_id
        )
