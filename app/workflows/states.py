from app.models.entities import EventStatus
ERROR="error"
TRANSITIONS={EventStatus.CREATED:{EventStatus.CLASSIFIED,ERROR},EventStatus.CLASSIFIED:{EventStatus.PLANNING,ERROR},EventStatus.PLANNING:{EventStatus.AWAITING_APPROVAL,ERROR},EventStatus.AWAITING_APPROVAL:{EventStatus.APPROVED,EventStatus.REJECTED,ERROR},EventStatus.APPROVED:{EventStatus.EXECUTING,ERROR},EventStatus.EXECUTING:{EventStatus.MONITORING,ERROR},EventStatus.MONITORING:{EventStatus.COMPLETED,ERROR},EventStatus.COMPLETED:{EventStatus.ARCHIVED,ERROR},EventStatus.ARCHIVED:{ERROR},ERROR:{}}
def can_transition(current, target): return target in TRANSITIONS.get(current,set())
