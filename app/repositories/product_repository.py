from typing import Protocol
class ProductRepository(Protocol):
    async def by_supplier(self, vendor_id: str) -> list[dict]: ...
    async def by_factory(self, factory_id: str) -> list[dict]: ...
class InMemoryProductRepository:
    def __init__(self, products=None): self.products=products or []
    async def by_supplier(self, vendor_id): return [p for p in self.products if p.get("vendor_id")==vendor_id]
    async def by_factory(self, factory_id): return [p for p in self.products if p.get("factory_id")==factory_id]
