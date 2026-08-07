from app.services.llm import LLMProvider, LLMResponse, LLMService
from app.schemas.agents import VendorRankingOutput
class FakeProvider(LLMProvider):
    name="fake"
    async def complete(self,prompt,**kwargs):
        return LLMResponse('{"primary_vendor":{"vendor_id":"v1","vendor_name":"A","score":0.9,"estimated_cost":10,"delivery_days":2,"confidence":0.9},"alternatives":[],"recommendation":"use v1"}',10,.001,"fake-model","fake",1)
async def test_structured_llm_output_parses():
    result,response=await LLMService([FakeProvider()]).call_structured("rank",VendorRankingOutput)
    assert result.primary_vendor.vendor_id=="v1" and response.tokens_used==10
