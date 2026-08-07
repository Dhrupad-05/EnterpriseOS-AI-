async def check_database(db):
    try: await db.execute("SELECT 1"); return {"status":"ok"}
    except Exception as exc: return {"status":"degraded","error":type(exc).__name__}
async def check_redis(redis):
    try: await redis.ping(); return {"status":"ok"}
    except Exception as exc: return {"status":"degraded","error":type(exc).__name__}
