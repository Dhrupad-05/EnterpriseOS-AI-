from app.agents.contract import Agent
from app.schemas.agents import VendorQuery, VendorRecommendation
class VendorIntelligenceAgent(Agent[VendorQuery, list[VendorRecommendation]]):
    name="vendor_intelligence"; description="Ranks vendors using delivery, cost, and risk signals."; input_schema=VendorQuery; output_schema=list[VendorRecommendation]
    instructions="Score delivery performance at 80%, cost competitiveness at 10%, and risk at 10%; expose delay risk and alternatives."
    confidence_threshold=.5
    async def run(self,value):
        candidates=value.candidates or [{"id":"vendor-a","name":"Vendor A","performance":.92,"cost":.88,"risk":.08,"days":3},{"id":"vendor-b","name":"Vendor B","performance":.84,"cost":.94,"risk":.12,"days":5},{"id":"vendor-c","name":"Vendor C","performance":.76,"cost":.98,"risk":.22,"days":7}]
        results=[]
        for item in candidates:
            score=.8*item["performance"]+.1*item["cost"]+.1*(1-item["risk"])
            results.append(VendorRecommendation(vendor_id=item["id"],vendor_name=item["name"],score=score,estimated_cost=value.budget/max(value.quantity,1),delivery_days=item["days"],confidence=min(.99,score),risk_flags=["delay-risk"] if item["days"]>5 else []))
        return sorted(results,key=lambda x:x.score,reverse=True)[:3]
