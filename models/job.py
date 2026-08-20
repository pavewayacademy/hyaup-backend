from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from config.database import Base
class Job(Base):
  __tablename__ = "jobs"
  # Core Primary Key
  id = Column(Integer,primary_key=True, index=True)
  # Standard Metadata Fields
  title = Column(String(255), nullable=False)
  company = Column(String(255), nullable=False)
  location = Column(String(255), nullable=True)
  description = Column(Text, nullable=True)
  status = Column(String(50), default="active", nullable=False)
  url = Column(String(500), nullable=True)
  source = Column(String(100), nullable=True)
  # Vector Embedding Column (Stores float-point array structures as JSON)
  # Example format: [0.0123, -0.0456, 0.7890, ...]
  embedding = Column(JSON, nullable=True)
  # Timestamps
  created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
  def __repr__(self):
    return f"<Job(id={self.id}, title='{self.title}', company='{self.company}')>"
