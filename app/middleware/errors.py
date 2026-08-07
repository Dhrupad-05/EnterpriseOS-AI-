from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import EnterpriseError, NotFoundError, PolicyViolationError
async def enterprise_exception_handler(request:Request,exc:EnterpriseError):
    status=404 if isinstance(exc,NotFoundError) else 422 if isinstance(exc,PolicyViolationError) else 400
    return JSONResponse(status_code=status,content={"error":exc.__class__.__name__,"detail":str(exc)})
