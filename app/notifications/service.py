from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol
import httpx
from tenacity import AsyncRetrying, retry_if_exception_type, stop_after_attempt, wait_exponential
from app.config.settings import get_settings
class Channel(Protocol):
    name: str
    async def send(self, recipient: str, subject: str, body: str) -> None: ...
@dataclass
class NotificationResult:
    channel: str; recipient: str; delivered: bool; error: str|None=None
class NotificationService:
    """Injectable notification ports plus real Resend and Slack adapters when credentials are configured."""
    def __init__(self, channels: dict[str,Channel] | None=None): self.channels=channels or {}; self.settings=get_settings()
    async def send(self,channel,recipient,subject,body):
        adapter=self.channels.get(channel)
        if adapter:
            try:
                async for attempt in AsyncRetrying(stop=stop_after_attempt(3),wait=wait_exponential(multiplier=.2,max=2),retry=retry_if_exception_type((TimeoutError,ConnectionError)),reraise=True):
                    with attempt: await adapter.send(recipient,subject,body)
                return NotificationResult(channel,recipient,True)
            except Exception as exc: return NotificationResult(channel,recipient,False,type(exc).__name__)
        if channel=="email": return await self._send_resend(recipient,subject,body)
        if channel=="slack": return await self._send_slack(recipient,body)
        return NotificationResult(channel,recipient,False,"channel_not_configured")
    async def send_approval_request(self,approval,recipient):
        minutes=max(0,int((approval.expires_at-datetime.now(timezone.utc)).total_seconds()/60)) if approval.expires_at else 30
        body=f"Approval required: {approval.proposed_action}. Expires in {minutes} minutes. Approve or reject in EnterpriseOS."
        return [await self.send("email",recipient,"Approval Required",body),await self.send("slack","#approvals",body,body)]
    async def _send_resend(self,recipient,subject,body):
        if not self.settings.resend_api_key: return NotificationResult("email",recipient,False,"resend_not_configured")
        async with httpx.AsyncClient(timeout=10) as client:
            response=await client.post("https://api.resend.com/emails",headers={"Authorization":f"Bearer {self.settings.resend_api_key}"},json={"from":self.settings.notification_from_email,"to":[recipient],"subject":subject,"html":f"<p>{body}</p>"})
            return NotificationResult("email",recipient,response.is_success,None if response.is_success else response.text)
    async def _send_slack(self,channel,text):
        if not self.settings.slack_bot_token: return NotificationResult("slack",channel,False,"slack_not_configured")
        async with httpx.AsyncClient(timeout=10) as client:
            response=await client.post("https://slack.com/api/chat.postMessage",headers={"Authorization":f"Bearer {self.settings.slack_bot_token}"},json={"channel":channel,"text":text})
            success=response.is_success and response.json().get("ok",False)
            return NotificationResult("slack",channel,success,None if success else response.text)
