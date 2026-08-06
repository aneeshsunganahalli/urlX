from typing import Annotated

from fastapi import Depends, Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from cache import get_client

DatabaseDep = Annotated[AsyncSession, Depends(get_db)]
RedisDep = Annotated[Redis, Depends(get_client)]

def get_worker_id(request: Request) -> int:
    """
    Returns the worker_id of the server instance.
    """
    
    return request.app.state.worker_id