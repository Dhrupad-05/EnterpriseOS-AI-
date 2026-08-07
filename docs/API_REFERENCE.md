# API reference

FastAPI generates the authoritative OpenAPI contract at `/openapi.json` and `/docs`.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Liveness check |
| POST | `/api/v1/auth/login` | Issue access and refresh JWTs |
| POST | `/api/v1/events` | Ingest a Business Event |
| GET | `/api/v1/system/metrics` | Runtime counters and latency observations |

Example event:

```json
{"event_type":"VendorBankruptcy","title":"Critical supplier failed","description":"Primary supplier entered bankruptcy","severity":"critical","payload":{"daily_loss":2300000,"employees_affected":500,"recovery_budget":100000}}
```

All protected endpoints require `Authorization: Bearer <access_token>` and return a correlation ID in `X-Correlation-ID`.
