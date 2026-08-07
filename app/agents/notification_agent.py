from app.agents.contract import Agent
from app.schemas.agents import BusinessEventInput
from app.notifications.service import NotificationService
class NotificationAgent(Agent[BusinessEventInput, dict]):
    name="notification"; description="Routes role-aware notifications through injected channel adapters."; input_schema=BusinessEventInput; output_schema=dict
    instructions="Select email, Slack, SMS, or push based on urgency and recipient role; retry transient delivery failures. Never approve or execute."
    def __init__(self, service=None): self.service=service or NotificationService()
    async def run(self,value):
        channels=value.payload.get("notification_channels",["email"]); recipient=value.payload.get("recipient","operations@company.com"); subject=f"EnterpriseOS event: {value.title}"; body=value.description; results=[]
        for channel in channels: results.append((await self.service.send(channel,recipient,subject,body)).__dict__)
        return {"queued":False,"channels":results,"audience":value.payload.get("audience_roles",["operations"])}
