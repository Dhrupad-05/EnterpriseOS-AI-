from app.agents.contract import Agent
from app.schemas.agents import VendorQuery, VendorRecommendation, VendorRankingOutput
from app.repositories.vendor_repository import InMemoryVendorRepository
class VendorIntelligenceAgent(Agent[VendorQuery, list[VendorRecommendation]]):
    name="vendor_intelligence"; description="Ranks vendors using delivery, cost, and risk signals."; input_schema=VendorQuery; output_schema=list[VendorRecommendation]
    instructions="Score delivery performance at 80%, cost competitiveness at 10%, and risk at 10%; expose delay risk and alternatives."
    confidence_threshold=.5
    def __init__(self, repository=None, llm_service=None): self.repository=repository or InMemoryVendorRepository(); self.llm=llm_service
    async def run(self,value):
        repository_candidates=await self.repository.list_by_category(value.category)
        candidates=value.candidates or [{"id":v.vendor_id,"name":v.name,"performance":v.on_time_deliveries/max(v.total_orders,1),"cost":1/(1+v.avg_unit_cost),"risk":v.late_deliveries/max(v.total_orders,1),"days":v.avg_delivery_days} for v in repository_candidates]
        candidates=candidates or [{"id":"vendor-a","name":"Vendor A","performance":.92,"cost":.88,"risk":.08,"days":3},{"id":"vendor-b","name":"Vendor B","performance":.84,"cost":.94,"risk":.12,"days":5},{"id":"vendor-c","name":"Vendor C","performance":.76,"cost":.98,"risk":.22,"days":7}]
        if self.llm:
            try:
                output,_=await self.llm.call_structured(f"Rank these vendors for {value.category}, quantity {value.quantity}, budget {value.budget}: {candidates}",VendorRankingOutput)
                return [output.primary_vendor,*output.alternatives][:3]
            except RuntimeError:
                pass
        results=[]
        for item in candidates:
            score=.8*item["performance"]+.1*item["cost"]+.1*(1-item["risk"])
            results.append(VendorRecommendation(vendor_id=item["id"],vendor_name=item["name"],score=score,estimated_cost=value.budget/max(value.quantity,1),delivery_days=item["days"],confidence=min(.99,score),risk_flags=["delay-risk"] if item["days"]>5 else []))
        return sorted(results,key=lambda x:x.score,reverse=True)[:3]
