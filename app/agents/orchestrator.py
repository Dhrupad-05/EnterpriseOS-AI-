from app.agents.coo_agent import COOAgent
from app.agents.crisis_agent import CrisisAgent
from app.agents.finance_agent import FinanceAgent
from app.agents.compliance_agent import ComplianceAgent
from app.agents.operations_agent import OperationsAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.procurement_agent import ProcurementAgent
from app.agents.vendor_intelligence_agent import VendorIntelligenceAgent
class AgentOrchestrator:
    def __init__(self): self.agents={a.name:a for a in [COOAgent(),CrisisAgent(),FinanceAgent(),ComplianceAgent(),OperationsAgent(),PlannerAgent(),ProcurementAgent(),VendorIntelligenceAgent()]}
    def get(self,name): return self.agents[name]
