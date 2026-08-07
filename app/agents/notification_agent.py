from app.agents.contract import Agent
from app.schemas.agents import BusinessEventInput
class NotificationAgent(Agent[BusinessEventInput, dict]):
    name="notification"; description="Routes role-aware notifications through injected channel adapters."; input_schema=BusinessEventInput; output_schema=dict
    instructions="Select email, Slack, SMS, or push based on urgency and recipient role; retry transient delivery failures. Never approve or execute."
    async def run(self,value): return {"queued":True,"channels":value.payload.get("notification_channels",["email"]),"audience":value.payload.get("audience_roles",["operations"])}
