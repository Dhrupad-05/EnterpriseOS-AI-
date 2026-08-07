from fastapi import FastAPI
from app.core.logging import configure_logging
from app.core.exceptions import EnterpriseError
from app.middleware.errors import enterprise_exception_handler
from app.api.routes import health, events, auth, system, approvals, workflows
from app.middleware.correlation import CorrelationIdMiddleware
configure_logging()
app=FastAPI(title="EnterpriseOS AI",version="0.1.0",description="The Operating System for Autonomous Enterprises")
app.add_middleware(CorrelationIdMiddleware)
app.include_router(health.router,tags=["System"]); app.include_router(events.router,prefix="/api/v1")
app.include_router(auth.router,prefix="/api/v1")
app.include_router(system.router,prefix="/api/v1"); app.add_exception_handler(EnterpriseError,enterprise_exception_handler)
app.include_router(approvals.router,prefix="/api/v1")
app.include_router(workflows.router,prefix="/api/v1")
