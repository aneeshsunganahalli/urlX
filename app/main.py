from fastapi import FastAPI, Depends, status, HTTPException
from routers import generate
from sqlalchemy.orm import Session
from sqlalchemy import text
import redis

from database import get_db

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

app = FastAPI()
app.include_router(generate.router)

@app.get("/")
def root():
    return {"API is running."}

@app.get("/health-check")
def health_check(db: Session = Depends(get_db)):
    try:
        # Check database health
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )



    
    