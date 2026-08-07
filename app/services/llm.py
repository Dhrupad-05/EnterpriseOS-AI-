import json
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, TypeVar
import httpx
from pydantic import BaseModel
from tenacity import AsyncRetrying, retry_if_exception_type, stop_after_attempt, wait_exponential
from app.config.settings import get_settings

T=TypeVar("T",bound=BaseModel)
@dataclass
class LLMResponse:
    content: str; tokens_used: int; cost_usd: float; model: str; provider: str; latency_ms: int
class LLMProvider(ABC):
    name="provider"
    @abstractmethod
    async def complete(self,prompt:str,**kwargs:Any)->LLMResponse: ...
class HTTPChatProvider(LLMProvider):
    def __init__(self,name,url,api_key,model,price_in=0.0,price_out=0.0): self.name=name; self.url=url; self.api_key=api_key; self.model=model; self.price_in=price_in; self.price_out=price_out
    async def complete(self,prompt,**kwargs):
        if not self.api_key: raise RuntimeError(f"{self.name} API key is not configured")
        started=time.perf_counter()
        async with httpx.AsyncClient(timeout=5) as client:
            response=await client.post(self.url,headers={"Authorization":f"Bearer {self.api_key}","Content-Type":"application/json"},json={"model":self.model,"messages":[{"role":"user","content":prompt}],"temperature":kwargs.get("temperature",.3),"max_tokens":kwargs.get("max_tokens",2000),"response_format":{"type":"json_object"}})
            response.raise_for_status(); data=response.json(); usage=data.get("usage",{}); input_tokens=int(usage.get("prompt_tokens",0)); output_tokens=int(usage.get("completion_tokens",0)); return LLMResponse(data["choices"][0]["message"]["content"],input_tokens+output_tokens,(input_tokens/1e6)*self.price_in+(output_tokens/1e6)*self.price_out,self.model,self.name,round((time.perf_counter()-started)*1000))
class GeminiProvider(LLMProvider):
    name="gemini"
    def __init__(self,api_key=None,model="gemini-2.5-flash"): self.api_key=api_key; self.model=model
    async def complete(self,prompt,**kwargs):
        if not self.api_key: raise RuntimeError("gemini API key is not configured")
        started=time.perf_counter(); url=f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        async with httpx.AsyncClient(timeout=5) as client:
            response=await client.post(url,json={"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"temperature":kwargs.get("temperature",.3),"maxOutputTokens":kwargs.get("max_tokens",2000),"responseMimeType":"application/json"}}); response.raise_for_status(); data=response.json(); text=data["candidates"][0]["content"]["parts"][0]["text"]; usage=data.get("usageMetadata",{}); tokens=sum(int(usage.get(k,0)) for k in ("promptTokenCount","candidatesTokenCount")); return LLMResponse(text,tokens,0.0,self.model,self.name,round((time.perf_counter()-started)*1000))
class LLMService:
    """Structured Gemini -> Groq -> OpenRouter service. Deterministic agents remain usable when keys are absent."""
    def __init__(self,providers=None):
        settings=get_settings(); self.providers=providers or [GeminiProvider(settings.gemini_api_key),HTTPChatProvider("groq","https://api.groq.com/openai/v1/chat/completions",settings.groq_api_key,"llama-3.1-8b-instant",.24,.24),HTTPChatProvider("openrouter","https://openrouter.ai/api/v1/chat/completions",settings.openrouter_api_key,"meta-llama/llama-3.1-8b-instruct",.08,.08)]
    async def call_structured(self,prompt:str,output_schema:type[T],temperature=.3)->tuple[T,LLMResponse]:
        schema=json.dumps(output_schema.model_json_schema())
        last=None
        for provider in self.providers:
            try:
                async for attempt in AsyncRetrying(stop=stop_after_attempt(3),wait=wait_exponential(multiplier=.2,max=2),retry=retry_if_exception_type((TimeoutError,ConnectionError,httpx.HTTPError)),reraise=True):
                    with attempt: response=await provider.complete(f"{prompt}\nReturn only JSON matching this schema:\n{schema}",temperature=temperature,max_tokens=2000)
                return output_schema.model_validate(json.loads(response.content)),response
            except Exception as exc: last=exc
        raise RuntimeError("All LLM providers failed") from last
