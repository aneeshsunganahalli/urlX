import uuid
from sqlalchemy import Column, Integer, Text, UUID, VARCHAR, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base


class URLs(Base):
  __tablename__ = "URLs"
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid())
  short_url = Column(VARCHAR(20), unique=True, nullable=False, index=True)
  original_url = Column(Text, unique=True, nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
  click_count = Column(Integer, default=0, server_default="0")
  
  analytics = relationship("Analytics", back_populates='url',cascade="all, delete-orphan")
  