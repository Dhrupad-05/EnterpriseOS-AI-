from fastapi import APIRouter
from app.observability import metrics as app_metrics
router=APIRouter(prefix="/system",tags=["System"])
@router.get("/metrics")
async def metrics(): return {"status":"ok","metrics":app_metrics.snapshot()}
