from uuid import UUID
from pydantic import BaseModel, HttpUrl
from datetime import datetime

class URLBase(BaseModel):
    original_url: HttpUrl

class URLCreate(URLBase):
    pass

class URLResponse(URLBase):
    id: UUID
    short_url: str
    created_at: datetime
    click_count: int
    
    model_config = {"from_attributes": True}

