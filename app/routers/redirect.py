from typing import Annotated
import json

from fastapi import APIRouter, HTTPException, status, BackgroundTasks, Header
from fastapi.responses import RedirectResponse
from sqlalchemy import select, insert
from user_agents import parse

from deps import DatabaseDep
from database import AsyncSessionLocal
from models import URLs, Analytics
from cache import get, set, increment_and_mark

router = APIRouter(tags=["Redirects"])

async def process_analytics(short_url: str, user_agent: str | None, url_id: str):
  
    parsed_ua = parse(user_agent) if user_agent else None
    
    analytics_data = {
        "url_id" : url_id,
        "browser": parsed_ua.browser.family if parsed_ua else "Unknown",
        "os": parsed_ua.os.family if parsed_ua else "Unknown",
        "device": parsed_ua.device.family if parsed_ua else "Unknown",
    }
    
    async with AsyncSessionLocal() as db_session:
        stmt = insert(Analytics).values(**analytics_data)
        await db_session.execute(stmt)
        await db_session.commit()
    
    await increment_and_mark(short_url)


@router.get("/{short_url}")
async def redirect(short_url: str, db: DatabaseDep, user_agent: Annotated[str | None, Header()], background_tasks: BackgroundTasks):
  # Check Cache
  cache_hit = await get(short_url)
  
  if cache_hit:
    data = json.loads(cache_hit)
    destination_url = data["destination_url"]
    url_id = data["url_id"]
  
  else:
    # Check DB
    stmt = select(URLs).where(URLs.short_url == short_url)
    result = await db.execute(stmt)
    existing_url = result.scalar()
    
    if not existing_url:
      raise HTTPException(
                  status_code=status.HTTP_404_NOT_FOUND,
                  detail="Key not found in database"
                )
      
    destination_url = existing_url.original_url
    url_id = str(existing_url.id)
  
  
    if not destination_url.startswith(("http://", "https://")):
        destination_url = f"https://{destination_url}"
    
    cache_data = json.dumps({
    "destination_url": destination_url, 
    "url_id": url_id
})
      
    await set(short_url, cache_data, 86400)
  
  
  background_tasks.add_task(process_analytics, short_url, user_agent, url_id)
  
  return RedirectResponse(url=destination_url, status_code=302)