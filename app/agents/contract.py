import asyncio
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from pydantic import BaseModel
from tenacity import AsyncRetrying, retry_if_exception_type, stop_after_attempt, wait_exponential

InputT = TypeVar("InputT", bound=BaseModel)
OutputT = TypeVar("OutputT", bound=BaseModel)

class Agent(ABC, Generic[InputT, OutputT]):
    name: str
    description: str
    input_schema: type[InputT]
    output_schema: type[OutputT]
    instructions: str
    tools: list[object] = []
    confidence_threshold: float = 0.7
    timeout_seconds: int = 30
    max_retries: int = 2
    dependencies: list["Agent"] = []

    async def execute(self, raw_input: InputT | dict) -> OutputT:
        validated = raw_input if isinstance(raw_input, self.input_schema) else self.input_schema.model_validate(raw_input)
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(self.max_retries + 1),
            wait=wait_exponential(multiplier=0.2, min=0.2, max=2),
            retry=retry_if_exception_type((TimeoutError, ConnectionError)),
            reraise=True,
        ):
            with attempt:
                result = await asyncio.wait_for(self.run(validated), timeout=self.timeout_seconds)
                if hasattr(result, "confidence") and result.confidence < self.confidence_threshold:
                    raise ValueError(f"{self.name} confidence below threshold")
                return result
        raise RuntimeError(f"{self.name} did not return a result after retries")

    @abstractmethod
    async def run(self, value: InputT) -> OutputT: ...
