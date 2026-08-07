from uuid import uuid4
from app.approvals.queue import ApprovalQueue
async def test_approval_queue_expires():
    queue=ApprovalQueue(); request=await queue.await_approval(uuid4(),"test",{},timeout_minutes=0); request=queue.resume(request.id,"approved")
    assert request.decision=="expired"
