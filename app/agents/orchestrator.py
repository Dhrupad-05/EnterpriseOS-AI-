from app.agents.coo_agent import COOAgent
from app.agents.crisis_agent import CrisisAgent
from app.agents.finance_agent import FinanceAgent
from app.agents.compliance_agent import ComplianceAgent
from app.agents.operations_agent import OperationsAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.procurement_agent import ProcurementAgent
from app.agents.vendor_intelligence_agent import VendorIntelligenceAgent
from app.services.llm import LLMService
class AgentOrchestrator:
    def __init__(self,llm_service=None):
        llm=llm_service or LLMService(); vendor=VendorIntelligenceAgent(llm_service=llm)
        self.agents={a.name:a for a in [COOAgent(),CrisisAgent(vendor_agent=vendor),FinanceAgent(),ComplianceAgent(),OperationsAgent(),PlannerAgent(),ProcurementAgent()]}; self.agents[vendor.name]=vendor
    def get(self,name): return self.agents[name]
