import time
from dataclasses import dataclass

from mistralai.client import Mistral

from src.core.exceptions import EmptyAPIResponseError

DEFAULT_MODEL = "mistral-small-latest"


@dataclass(slots=True)
class LLMResult:
    content: str
    model: str
    input_tokens: int | None
    output_tokens: int | None
    latency_ms: int


class MistralProvider:
    def __init__(self, api_key: str) -> None:
        self._api_key: str = api_key
        self._client: Mistral | None = None

    @property
    def client(self) -> Mistral:
        if self._client is None:
            self._client = Mistral(api_key=self._api_key)
        return self._client

    async def complete(
        self,
        messages: list[dict],
        model: str = DEFAULT_MODEL,
    ) -> LLMResult:
        started = time.perf_counter()

        response = await self.client.chat.complete_async(
            model=model,
            messages=messages,
        )

        latency_ms = int((time.perf_counter() - started) * 1000)

        if not response.choices or not response.choices[0].message.content:
            raise EmptyAPIResponseError("LLM returned an empty response")

        usage = response.usage

        return LLMResult(
            content=response.choices[0].message.content,
            model=response.model or model,
            input_tokens=getattr(usage, "prompt_tokens", None),
            output_tokens=getattr(usage, "completion_tokens", None),
            latency_ms=latency_ms,
        )
