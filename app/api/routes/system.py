from fastapi import APIRouter
from app.observability import metrics as app_metrics
from app.observability.prometheus import metrics_response
router=APIRouter(prefix="/system",tags=["System"])
@router.get("/metrics")
async def metrics(): return {"status":"ok","metrics":app_metrics.snapshot()}
@router.get("/metrics/prometheus",include_in_schema=False)
async def prometheus_metrics(): return metrics_response()
