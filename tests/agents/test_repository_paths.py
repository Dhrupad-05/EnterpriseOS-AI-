from app.agents.vendor_intelligence_agent import VendorIntelligenceAgent
from app.repositories.vendor_repository import InMemoryVendorRepository, VendorMetrics
from app.schemas.agents import VendorQuery
async def test_vendor_repository_metrics_drive_ranking():
    repo=InMemoryVendorRepository([VendorMetrics("v1","Reliable","parts",90,100,10,95,2,2),VendorMetrics("v2","Risky","parts",50,100,8,70,8,30)])
    result=await VendorIntelligenceAgent(repo).execute(VendorQuery(category="parts",quantity=10,budget=1000))
    assert result[0].vendor_id=="v1" and result[0].delivery_days==2
