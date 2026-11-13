from pydantic import BaseModel

from src.dto.agent.model_selection.mistral_selection import MistralSelection


class SelectionLLM(BaseModel):
    mistral: MistralSelection

    @property
    def model_name(self) -> str:
        return self.mistral.value

