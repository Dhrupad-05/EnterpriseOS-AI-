from app.core.exceptions import ApprovalRequiredError
from app.models.entities import ApprovalStatus
class ApprovalService:
    def ensure_decided(self,approval):
        if approval.status == ApprovalStatus.PENDING: raise ApprovalRequiredError("Human approval is required")
        return approval.status == ApprovalStatus.APPROVED
