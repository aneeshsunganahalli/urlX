from uuid import UUID
from pydantic import BaseModel, HttpUrl, field_validator
from datetime import datetime
from url_normalize import url_normalize as normalize

class URLBase(BaseModel):
    original_url: HttpUrl
    
    @field_validator('original_url', mode='before')
    @classmethod
    
    def normalize_url(cls, value: str) -> HttpUrl:
        if isinstance(value, str):  
                    normalized_url = normalize(value)
                    return normalized_url
        return value
                
class URLCreate(URLBase):
    pass

class URLResponse(URLBase):
    id: UUID
    short_url: str
    created_at: datetime
    click_count: int
    
    model_config = {"from_attributes": True}



