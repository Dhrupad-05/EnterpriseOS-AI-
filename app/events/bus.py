from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable
@dataclass(frozen=True)
class DomainEvent: name: str; payload: dict[str,Any] = field(default_factory=dict)
class EventBus:
    def __init__(self): self._handlers: dict[str,list[Callable[[DomainEvent],Awaitable[None]]]]={}
    def subscribe(self,name,handler): self._handlers.setdefault(name,[]).append(handler)
    async def publish(self,event: DomainEvent):
        for handler in self._handlers.get(event.name,[]): await handler(event)
