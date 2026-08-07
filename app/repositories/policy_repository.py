from typing import Protocol
class PolicyRepository(Protocol):
    async def active(self) -> list[dict]: ...
class InMemoryPolicyRepository:
    def __init__(self, policies=None): self.policies=policies or []
    async def active(self): return [p for p in self.policies if p.get("active",True)]
