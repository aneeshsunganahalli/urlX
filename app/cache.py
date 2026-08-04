from redis.asyncio import Redis
from redis.typing import KeyT, EncodableT

from sqlalchemy import update, bindparam

from models import URLs
from database import AsyncSessionLocal


redis: Redis | None = None

async def connect() -> None:
  global redis
  
  redis = Redis(
    host='localhost', 
    port=6379, 
    db=0,
    decode_responses=True
    )
  
  await redis.ping()

async def disconnect() -> None:
  global redis
  if redis is not None:
        await redis.aclose()
        redis = None
  
async def get_client() -> Redis:
  if redis is None:
    raise RuntimeError("Redis client is not initialized. Call connect() first.")
  return redis

async def get(key: KeyT) -> str | None:
    return await get_client().get(key)

async def set(
    key: KeyT, 
    value: EncodableT, 
    expire_seconds: int | None = None
) -> bool | None:
    return await get_client().set(key, value, ex=expire_seconds)


async def increment_and_mark(short_url: str) -> int:
  
  count_key = f"{short_url}:count"
  client = await get_client()
  pipe = client.pipeline()
  
  pipe.incr(count_key)
  pipe.sadd("dirty_urls", short_url)
  result = await pipe.execute()
  
  return result[0]

  
async def cron():
  client = await get_client()
  
  async with AsyncSessionLocal() as db:
    while True:
      dirty_set =  await client.spop("dirty_urls", count=100)
      
      if not dirty_set:
        break
    
      payload = []
      keys_to_delete = []
      
      for url in dirty_set:
        count_key = f"{url}:count"
        amount = await get(count_key)
        
        if amount is None:
          continue
        
        payload.append({
          "short_url":  url,
          "click_count": int(amount)
        })
        keys_to_delete.append(count_key)
        
      if not payload:
        continue
      
      stmt = update(URLs).where(URLs.short_url == bindparam("short_url")).values(click_count = URLs.click_count + bindparam("click_count"))
      
      try:
        await db.execute(stmt, payload)  
        await db.commit()
        
        if keys_to_delete:
          await client.delete(*keys_to_delete)
      
      except Exception as e:
        await db.rollback()
        
        # Adding failed URLs back to dirty_urls so they aren't lost
        await client.sadd("dirty_urls", *dirty_set)
        print(f"Cron batch failed and rolled back: {e}")