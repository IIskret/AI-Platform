from pydantic import BaseModel, Field

from typing import Optional


class UpdateAgent(BaseModel):
    name: Optional[str] = Field(
        min_length=1,
        max_length=128,
        default=None
    )
    description: Optional[str] = Field(
        default=None
    )
    system_prompt: Optional[str] = Field(
        default=None
    )
    model: Optional[str] = Field(
        min_length=1,
        default=None
    )
    temperature: Optional[float] = Field(
        ge=0.1,
        le=2.0,
        default=None
    )