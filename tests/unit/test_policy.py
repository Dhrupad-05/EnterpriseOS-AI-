from app.services.policy import PolicyEngine
def test_budget_policy():
    result=PolicyEngine().evaluate({"severity":"low","payload":{"amount":101}},[{"name":"finance","rules":{"budget_limit":100}}])
    assert not result.permitted
