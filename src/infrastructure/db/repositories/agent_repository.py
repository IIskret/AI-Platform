from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID

from src.infrastructure.db.models.agent_schema import Agent
from src.infrastructure.logging.logger import logger
from src.core.exceptions import DataBaseExc
from src.core.exceptions import AgentNotFound
from src.dto.agent.agent_output import AgentOutput
from src.dto.agent.update_agent import UpdateAgent


class AgentRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(
        self,
        user_id: str,
        name: str,
        description: str,
        system_prompt: str,
        model: str,
        temperature: float
    ) -> AgentOutput:
        agent = Agent(
            user_id=user_id,
            name=name,
            description=description,
            system_prompt=system_prompt,
            model=model,
            temperature=temperature,
            prompt_version="v1",
            tools_version="v1"
        )
        self._session.add(agent)

        try:
            await self._session.flush()
            return AgentOutput(
                name=agent.name,
                description=agent.description,
                system_prompt=agent.system_prompt,
                model=agent.model,
                temperature=agent.temperature,
            )
        except SQLAlchemyError as e:
            logger.exception(
                f"Database exception: {e}"
            )
            raise DataBaseExc(
                "failed to create agent"
            )

    async def get_agents(
        self,
        user_id: str
    ) -> list[AgentOutput]:
        try:
            user_agents = select(Agent).where(
                Agent.user_id==user_id,
                Agent.is_active==True
            )
            get_agents = await self._session.scalars(user_agents)
            agents = get_agents.all()

            if not agents :
                raise AgentNotFound("Agents not found")
            return[
                AgentOutput(
                    agent_id=agent.id,
                    name=agent.name,
                    description=agent.description,
                    system_prompt=agent.system_prompt,
                    model=agent.model,
                    temperature=agent.temperature,
                )
                for agent in agents
            ]
        except SQLAlchemyError as e:
            logger.exception(
                f"Database exc: {e}"
            )
            raise DataBaseExc(
                "failed to get agents"
            )

    async def get_agent_by_id(
        self, 
        agent_id: UUID, 
        user_id: str
    ) -> AgentOutput | None:
        try:
            get_agent = select(Agent).where(
                Agent.id==agent_id,
                Agent.user_id==user_id
            )
            agent = await self._session.scalar(get_agent)

            if not agent:
                raise AgentNotFound("Agent not found")

            return AgentOutput(
                agent_id=agent.id,
                name=agent.name,
                description=agent.description,
                system_prompt=agent.system_prompt,
                model=agent.model,
                temperature=agent.temperature
            )
        except SQLAlchemyError as e:
            logger.exception(
                f"Database exc: {e}"
            )
            raise DataBaseExc(
                "failed to get agents"
            )

    async def update_agent(
        self,
        agent_id: str,
        user_id: str,
        schema: UpdateAgent
    ) -> AgentOutput:
        try:
            query = select(Agent).where(
                Agent.id==agent_id,
                Agent.user_id==user_id
            )
            agent = await self._session.scalar(query)

            if not agent:
                raise AgentNotFound("Agent not found")

            update_schema = schema.model_dump(exclude_unset=True)

            for key, value in update_schema.items():
                setattr(agent, key, value)

            await self._session.flush()

            return AgentOutput(
                name=agent.name,
                description=agent.description,
                system_prompt=agent.system_prompt,
                model=agent.model,
                temperature=agent.temperature
            )
        except SQLAlchemyError as e:
            logger.exception(
                f"Database exc: {e}"
            )
            raise DataBaseExc(
                "failed to update agent"
            )

    async def delete_agent(
        self,
        agent_id: str,
        user_id: str
    ):
        query = (
            update(Agent)
            .where(
                Agent.user_id==user_id,
                Agent.id==agent_id
            )
            .values(
                is_active=False
            )
        )

        await self._session.execute(query)
        return None



        
        


        
            
