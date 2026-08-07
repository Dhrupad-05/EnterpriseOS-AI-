from typing import Protocol
class IncidentRepository(Protocol):
    async def employees_affected(self, crisis_type: str, payload: dict) -> int: ...
    async def alternatives(self, vendor_id: str | None) -> list[dict]: ...
class InMemoryIncidentRepository:
    def __init__(self, employees=0, alternatives=None): self.employee_count=employees; self.alt=alternatives or []
    async def employees_affected(self, crisis_type, payload): return int(payload.get("employees_affected", self.employee_count))
    async def alternatives(self, vendor_id): return self.alt
