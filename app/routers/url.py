from fastapi import APIRouter
from threading import Lock
import time
from config import settings
import base62

CUSTOM_EPOCH = settings.custom_epoch
WORKER_ID = settings.worker_id

router = APIRouter(prefix = "/url", tags=["URL"])
  
@router.get("/shorten")
async def shorten_url():
  mutex = Lock()
  last_timestamp, sequence_number = 0, 0

  mutex.acquire()
  
  current_timestamp = int(time.time()) - CUSTOM_EPOCH
  if current_timestamp == last_timestamp:
    if  sequence_number == 4095:
      now = time.time()
      wait_time = 1.0 - (now % 1.0)
      time.sleep(wait_time)
      
      current_timestamp = int(time.time()) - CUSTOM_EPOCH
      last_timestamp = current_timestamp
      sequence_number = 0
    else:
      sequence_number += 1
    
  else:
    sequence_number = 0
    last_timestamp = current_timestamp
  
  
  snowflake_id = current_timestamp << 16 | WORKER_ID << 12 | sequence_number
  mutex.release()
  
  encoded_snowflake_id = base62.encode(snowflake_id)
  return encoded_snowflake_id
  
  
  
  