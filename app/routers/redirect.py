from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from fastapi.responses import RedirectResponse

from sqlalchemy import select

from deps import DatabaseDep
from models import URLs
from cache import get, set, increment_and_mark

router = APIRouter(tags=["Redirects"])

@router.get("/{short_url}")
async def redirect(short_url: str, db: DatabaseDep, background_tasks: BackgroundTasks):
  # Check Cache
  exists = await get(short_url)
  
  if exists is None:
    # Check DB
    stmt = select(URLs).where(URLs.short_url == short_url)
    result = await db.execute(stmt)
    existing_url = result.scalar()
    
    if not existing_url:
      raise HTTPException(
                  status_code=status.HTTP_404_NOT_FOUND,
                  detail="Key not found in database"
                )
      
    await set(short_url, existing_url.original_url, 86400)
    exists = existing_url.original_url
  
  background_tasks.add_task(increment_and_mark, short_url)
  
  return RedirectResponse(url=exists, status_code=302)