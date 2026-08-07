from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4
from dataclasses import dataclass
@dataclass
class ApprovalRequest:
    id: UUID; workflow_id: UUID; action: str; context: dict; requested_at: datetime; expires_at: datetime; decision: str|None=None; comment: str|None=None
class ApprovalQueue:
    def __init__(self, notifier=None): self.pending={}; self.notifier=notifier
    async def await_approval(self,workflow_id:UUID,action:str,context:dict,timeout_minutes=30):
        now=datetime.now(timezone.utc); req=ApprovalRequest(uuid4(),workflow_id,action,context,now,now+timedelta(minutes=timeout_minutes)); self.pending[req.id]=req
        if self.notifier: await self.notifier(req)
        return req
    def resume(self,approval_id:UUID,decision:str,comment=None):
        req=self.pending[approval_id]
        if datetime.now(timezone.utc)>req.expires_at: req.decision="expired"
        else: req.decision=decision; req.comment=comment
        return req
    async def check_and_escalate_expired(self):
        now=datetime.now(timezone.utc)
        for req in self.pending.values():
            if req.decision is None and req.expires_at<=now: req.decision="expired"
