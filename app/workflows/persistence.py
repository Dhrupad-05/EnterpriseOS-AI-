import json
from datetime import datetime, timezone
class StateSnapshotStore:
    """Dual-write snapshot adapter; Redis is fast replay cache, database audit is durable source."""
    def __init__(self, redis_client=None, audit_service=None): self.redis=redis_client; self.audit=audit_service
    async def save(self,workflow_id,state):
        payload=json.dumps({"saved_at":datetime.now(timezone.utc).isoformat(),"state":state},default=str)
        if self.redis: await self.redis.set(f"workflow:snapshot:{workflow_id}",payload)
        if self.audit: await self.audit.record(action="state_snapshot",correlation_id=str(workflow_id),decision=state)
    async def load(self,workflow_id):
        if not self.redis: return None
        raw=await self.redis.get(f"workflow:snapshot:{workflow_id}")
        return json.loads(raw)["state"] if raw else None
