import asyncio
import time
from abc import ABC, abstractmethod
from typing import Any
from tenacity import AsyncRetrying, retry_if_exception_type, stop_after_attempt, wait_exponential

class LLMProvider(ABC):
    name="provider"
    @abstractmethod
    async def complete(self,prompt:str,**kwargs:Any)->str: ...

class ConfiguredProvider(LLMProvider):
    def __init__(self,name,client=None): self.name=name; self.client=client
    async def complete(self,prompt,**kwargs):
        if not self.client: return f"{self.name} adapter ready; inject provider client in deployment."
        return await self.client.complete(prompt,**kwargs)

class CircuitBreaker:
    def __init__(self,failure_threshold=3,recovery_seconds=30): self.failure_threshold=failure_threshold; self.recovery_seconds=recovery_seconds; self.failures=0; self.opened_at=0.0
    def allow(self): return self.failures<self.failure_threshold or time.monotonic()-self.opened_at>=self.recovery_seconds
    def success(self): self.failures=0; self.opened_at=0.0
    def failure(self): self.failures+=1; self.opened_at=time.monotonic() if self.failures>=self.failure_threshold else self.opened_at

class LLMProviderChain:
    """Gemini -> Groq -> OpenRouter with 5s timeout, exponential retry, and per-provider breakers."""
    def __init__(self,providers=None):
        self.providers=providers or [ConfiguredProvider("gemini"),ConfiguredProvider("groq"),ConfiguredProvider("openrouter")]
        self.breakers={p.name:CircuitBreaker() for p in self.providers}
    async def complete(self,prompt,**kwargs):
        last=None
        for provider in self.providers:
            breaker=self.breakers[provider.name]
            if not breaker.allow(): continue
            try:
                async for attempt in AsyncRetrying(stop=stop_after_attempt(3),wait=wait_exponential(multiplier=.2,max=1),retry=retry_if_exception_type((TimeoutError,ConnectionError)),reraise=True):
                    with attempt: result=await asyncio.wait_for(provider.complete(prompt,**kwargs),timeout=5)
                breaker.success(); return result
            except Exception as exc:
                breaker.failure(); last=exc
        raise RuntimeError("All configured LLM providers failed") from last
