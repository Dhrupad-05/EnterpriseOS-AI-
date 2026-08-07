import pytest
from app.models.entities import EventStatus
from app.workflows.engine import WorkflowEngine
from app.core.exceptions import InvalidStateTransitionError
def test_valid_transition(): assert WorkflowEngine().transition(EventStatus.CREATED,EventStatus.CLASSIFIED)==EventStatus.CLASSIFIED
def test_invalid_transition():
    with pytest.raises(InvalidStateTransitionError): WorkflowEngine().transition(EventStatus.CREATED,EventStatus.COMPLETED)
