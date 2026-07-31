from sqlalchemy import Column, ForeignKey, UUID, VARCHAR, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base
import uuid

class Analytics(Base):
  __tablename__ = "Analytics"
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid())
  url_id = Column(UUID(as_uuid=True), ForeignKey("URLs.id", ondelete="cascade"), nullable=False)
  clicked_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
  device = Column(VARCHAR(100))
  os = Column(VARCHAR(30))
  browser = Column(VARCHAR(40))
  
  url = relationship("URLs", back_populates="analytics")