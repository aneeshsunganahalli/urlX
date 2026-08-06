from contextlib import asynccontextmanager

from fastapi import FastAPI, status, HTTPException, Request
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import text

from routers import generate, redirect
from database import Base, engine
from cache import connect, disconnect, cron, increment
from deps import DatabaseDep, RedisDep

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    await connect()
    
    worker_id = await increment("global_worker_counter")
    app.state.worker_id = worker_id % 64      # Keeping the modulo 2^(Worker_ID bits)
    
    
    scheduler = AsyncIOScheduler()
    scheduler.add_job(cron, "interval", seconds=60)
    scheduler.start()
    
    yield
    
    scheduler.shutdown()
    await disconnect()
    
app = FastAPI(lifespan=lifespan)

app.include_router(generate)
app.include_router(redirect)

@app.get("/")
def root(request: Request):
    return {"message": "API is running.", "workerID": request.app.state.worker_id}

@app.get("/db/health")
async def db_health_check(db: DatabaseDep):
    """
    Endpoint checks if there is a healthy connection to the Postgres Database
    """
    
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
    """
    Checks if there is a healthy connection to the Redis client
    """
    
    try:
        is_alive = await redis.ping()
        return {"status": "ok", "redis": is_alive}
    except Exception as e:
        return {"status": "error", "redis_error": str(e)}
    
@app.get("/worker/id")
def printer(request: Request):
    """
    Simple endpoint to retrieve an instance's worker_id
    """
    
    return {request.app.state.worker_id}