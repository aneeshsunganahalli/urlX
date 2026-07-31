from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from schemas import urls as urlSchema
from models import URLs
import time
from threading import Lock
from database import get_db
import base62
from config import settings
from sqlalchemy import select

CUSTOM_EPOCH = settings.custom_epoch
WORKER_ID = settings.worker_id

router = APIRouter(tags=["Generate"])

mutex = Lock()
last_timestamp, sequence_number = 0, 0

def get_current_time():
  return int(time.time()) - CUSTOM_EPOCH

def generate_snowflake_id():
    global last_timestamp, sequence_number
  
    with mutex:
      current_timestamp = get_current_time()
      if current_timestamp < last_timestamp:
            raise RuntimeError("Refine system time.")
          
      if current_timestamp == last_timestamp:
        sequence_number = (sequence_number + 1) & 4095
        if sequence_number == 0:
          while current_timestamp <= last_timestamp:
            time.sleep(0.01)
            current_timestamp = get_current_time()
        else:
          sequence_number += 1
      
      else:
        sequence_number = 0
      last_timestamp = current_timestamp

    snowflake_id = (current_timestamp << 16) | (WORKER_ID << 12) | sequence_number
    return snowflake_id



@router.post("/generate", response_model=urlSchema.URLResponse, status_code=status.HTTP_201_CREATED)
def generate_url(input_url: urlSchema.URLCreate, response: Response, db: Session = Depends(get_db)):
  
  # Check if the input URL already exists in the database
  target_url = str(input_url.original_url)
  
  stmt = select(URLs).where(URLs.original_url == target_url)
  exisiting_url = db.scalars(stmt).first()
  
  if exisiting_url:
    response.status_code=status.HTTP_200_OK
    return exisiting_url

  # Since it doesn't exist, we will create a new shortened URL
  try:
    snowflake_id = generate_snowflake_id()
  except RuntimeError as err:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=str(err)
    )
    
  encoded_snowflake_id = base62.encode(snowflake_id)
  
  db_url = URLs(
    short_url=encoded_snowflake_id, 
    original_url=str(input_url.original_url)
  )
 
  db.add(db_url)
  db.commit()
  db.refresh(db_url)
  
  return db_url



  
  
  
  