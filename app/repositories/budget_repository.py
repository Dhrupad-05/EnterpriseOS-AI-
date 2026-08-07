from typing import Protocol
class BudgetRepository(Protocol):
    async def department_budget(self, department: str) -> float: ...
    async def spending_to_date(self, department: str, period: str) -> float: ...
class InMemoryBudgetRepository:
    def __init__(self, budgets=None, spending=None): self.budgets=budgets or {}; self.spending=spending or {}
    async def department_budget(self, department): return float(self.budgets.get(department, 0))
    async def spending_to_date(self, department, period): return float(self.spending.get((department,period), 0))
