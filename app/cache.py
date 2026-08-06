from redis.asyncio import Redis
from redis.typing import KeyT, EncodableT

from sqlalchemy import update, bindparam

from models import URLs
from database import AsyncSessionLocal


redis: Redis | None = None

async def connect() -> None:
  """
  Starts the connection with Redis client and checks connection.
  """
  
  global redis
  
  redis = Redis(
    host='host.docker.internal', 
    port=6379, 
    db=0,
    decode_responses=True
    )
  
  await redis.ping()

async def disconnect() -> None:
  """
  Closes the Redis client connection.
  """
  
  global redis
  if redis is not None:
        await redis.aclose()
        redis = None
  
async def get_client() -> Redis:
  """
  Returns the client, used in dependency injection.
  """
  
  if redis is None:
    raise RuntimeError("Redis client is not initialized. Call connect() first.")
  return redis

async def get(key: KeyT) -> str | None:
  """
  Returns the value associated with provided key, else None
  """
  client = await get_client()
  if client is not None:
    return await client.get(key)

async def set(
    key: KeyT, 
    value: EncodableT, 
    expire_seconds: int | None = None
) -> bool | None:
  
  """
  Returns ok if value was set to provided key
  """
  
  client = await get_client()
  if client is not None:
    return await client.set(key, value, ex=expire_seconds)


async def increment_and_mark(short_url: str) -> int:
  """
  Increments the click count of a URL in Redis, and marks it for the cron job to check it.
  """
  
  count_key = f"{short_url}:count"
  client = await get_client()
  pipe = client.pipeline()
  
  pipe.incr(count_key)
  pipe.sadd("dirty_urls", short_url)
  result = await pipe.execute()
  
  return result[0]

async def increment(key: KeyT) -> int:
  """
  Increments a key's value.
  """
  
  client = await get_client()
  return await client.incr(key)

  
async def cron():
  """
  Cron job which bulk updates the click count of all marked URLs from the values stored in Redis, occurs every 60 seconds
  """
  client = await get_client()
  
  async with AsyncSessionLocal() as db:
    while True:
      dirty_set =  await client.spop("dirty_urls", count=100)
      
      if not dirty_set:
        break
      
      stmt = (
    update(URLs.__table__)  # Appending __table__ allows to bypass strict ORM for raw SQL bulk update
    .where(URLs.__table__.c.short_url == bindparam("b_short_url"))
    .values(click_count = URLs.__table__.c.click_count + bindparam("b_click_count"))
)
    
      payload = []
      keys_to_delete = []
      
      for url in dirty_set:
        count_key = f"{url}:count"
        amount = await get(count_key)
        
        if amount is None:
          continue
        
        payload.append({
          "b_short_url":  url,
          "b_click_count": int(amount)
        })
        keys_to_delete.append(count_key)
        
      if not payload:
        continue
      
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