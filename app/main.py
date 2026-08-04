from contextlib import asynccontextmanager

from fastapi import FastAPI, status, HTTPException, Header
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import text

from routers import generate, redirect
from database import Base, engine
from cache import connect, disconnect, cron
from deps import DatabaseDep, RedisDep

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    await connect()
    
    scheduler = AsyncIOScheduler()
    scheduler.add_job(cron, "interval", seconds=60)
    scheduler.start()
    
    yield
    
    scheduler.shutdown()
    await disconnect()
    
app = FastAPI(lifespan=lifespan)

app.include_router(generate.router)
app.include_router(redirect.router)

@app.get("/")
def root():
    return {"message": "API is running."}

@app.get("/db/health")
async def db_health_check(db: DatabaseDep):
    try:
        # Check database health
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )

@app.get("/redis/health")
async def redis_health_check(redis: RedisDep):
    try:
        is_alive = await redis.ping()
        return {"status": "ok", "redis": is_alive}
    except Exception as e:
        return {"status": "error", "redis_error": str(e)}