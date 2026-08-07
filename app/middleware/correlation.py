import uuid
from starlette.middleware.base import BaseHTTPMiddleware
class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request,call_next):
        correlation_id=request.headers.get("X-Correlation-ID",str(uuid.uuid4())); response=await call_next(request); response.headers["X-Correlation-ID"]=correlation_id; return response
