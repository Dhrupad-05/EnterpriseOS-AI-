from app.core.exceptions import InvalidStateTransitionError
from app.models.entities import EventStatus
from app.workflows.states import can_transition
class WorkflowEngine:
    def transition(self,current: EventStatus,target: EventStatus)->EventStatus:
        if not can_transition(current,target): raise InvalidStateTransitionError(f"{current} -> {target} is not allowed")
        return target
    def validate_definition(self, definition: dict) -> None:
        if not definition.get("steps"): raise ValueError("Workflow definition requires steps")
