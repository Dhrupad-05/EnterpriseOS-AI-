from app.workflows.states import can_transition
from app.models.entities import EventStatus
def test_replay_transition_path_is_deterministic():
    path=[EventStatus.CREATED,EventStatus.CLASSIFIED,EventStatus.PLANNING,EventStatus.POLICY_CHECK,EventStatus.AWAITING_APPROVAL,EventStatus.APPROVED,EventStatus.EXECUTING,EventStatus.MONITORING,EventStatus.COMPLETED,EventStatus.ARCHIVED]
    assert all(can_transition(a,b) for a,b in zip(path,path[1:]))
