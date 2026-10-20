from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.app.depends import get_agent_service, get_runs_service
from src.dto.agent.agent_output import AgentOutput
from src.dto.agent.create_agent import CreateAgent
from src.dto.agent.update_agent import UpdateAgent
from src.dto.runs.create_run import CreateRun
from src.dto.runs.run_output import RunOutput
from src.services.agent_service import AgentService
from src.services.runs_service import RunsService


agent_router = APIRouter(
    prefix="/agent",
    tags=["Agent"]
)

@agent_router.post("/create-agent", status_code=status.HTTP_201_CREATED)
async def create_agent(
    schema: CreateAgent,
    agent_service: AgentService = Depends(get_agent_service),
) -> AgentOutput:
    return await agent_service.create_agent(schema)

@agent_router.get("/get-agents", status_code=status.HTTP_200_OK)
async def get_agents(
    agent_service: AgentService = Depends(get_agent_service),
) -> list[AgentOutput]:
    return await agent_service.get_user_agents()

@agent_router.get("/get-agent/{id}", status_code=status.HTTP_200_OK)
async def get_agent_by_id(
    id: UUID,
    agent_service: AgentService = Depends(get_agent_service)
) -> AgentOutput:
    return await agent_service.agent_by_id(id)

@agent_router.patch("/update-agent/{id}", response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def update_agent(
    id: UUID,
    schema: UpdateAgent,
    agent_service: AgentService = Depends(get_agent_service)
) -> AgentOutput:
    return await agent_service.update_user_agent(
        agent_id=id,
        schema=schema
    )

@agent_router.patch("/delete-agent/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    id: UUID,
    agent_sercice: AgentService = Depends(get_agent_service)
) -> None:
    return await agent_sercice.delete_user_agent(agent_id=id)

@agent_router.post("/{id}/runs", status_code=status.HTTP_201_CREATED)
async def create_run(
    id: UUID,
    schema: CreateRun,
    runs_service: RunsService = Depends(get_runs_service)
) -> RunOutput:
    return await runs_service.create_run(agent_id=id, schema=schema)
