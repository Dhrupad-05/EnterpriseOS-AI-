class EnterpriseError(Exception): """Base application error."""
class NotFoundError(EnterpriseError): pass
class ConflictError(EnterpriseError): pass
class PolicyViolationError(EnterpriseError): pass
class ApprovalRequiredError(EnterpriseError): pass
class InvalidStateTransitionError(EnterpriseError): pass
class AuthenticationError(EnterpriseError): pass
