import pytest
from app.agents.procurement_agent import ProcurementAgent
from app.schemas.agents import BusinessEventInput
@pytest.mark.parametrize("event_type,payload",[("PurchaseRequest",{"amount":5000,"quantity":10}),("PurchaseRequest",{"amount":0}),("VendorDelay",{"amount":1200,"urgency":"rush"}),("PurchaseRequest",{"amount":100,"category":"safety"}),("VendorDelay",{"amount":900,"quantity":2}),("PurchaseRequest",{"amount":50000,"quantity":100}),("PurchaseRequest",{"amount":1,"quantity":1}),("VendorDelay",{"amount":2000,"vendor_status":"active"}),("PurchaseRequest",{"amount":7000,"urgency":"critical"}),("PurchaseRequest",{"amount":300,"candidates":[]})])
async def test_procurement_scenarios(event_type,payload):
    result=await ProcurementAgent().execute(BusinessEventInput(event_type=event_type,title="test",description="test",payload=payload))
    assert result.confidence >= .5 and result.alternatives
def test_invalid_event_contract():
    with pytest.raises(Exception): BusinessEventInput(event_type="",title="x",description="y")
