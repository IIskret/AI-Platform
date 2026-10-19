from pydantic import BaseModel, Field

from uuid import UUID

from typing import Optional


class CreateAgent(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=128
    )
    description: Optional[str] = Field(
        default=None
    )
    system_prompt: Optional[str] = Field(
        default=None
    )
    model: str = Field(
        min_length=1
    )
    temperature: float = Field(
        ge=0.1,
        le=2.0
    )