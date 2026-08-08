from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.responses import Response
WORKFLOWS=Counter("enterpriseos_workflows_total","Workflow outcomes",["status","event_type"])
AGENT_EXECUTIONS=Counter("enterpriseos_agent_executions_total","Agent outcomes",["agent","status"])
AGENT_LATENCY=Histogram("enterpriseos_agent_latency_ms","Agent latency in milliseconds",["agent"])
APPROVALS=Counter("enterpriseos_approvals_total","Approval decisions",["decision"])
def metrics_response(): return Response(generate_latest(),media_type=CONTENT_TYPE_LATEST)
