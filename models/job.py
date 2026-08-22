from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Base
from sqlalchemy import Column, Integer, String, Boolean

# The database model; maps to the database columns
class JobDB(Base):
    __tablename__ = "Jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), index=True, nullable=False) 
    jobType = Column(String(50), index=True, nullable=False)
    description = Column(String(1000), nullable=False)
    category = Column(String(100), nullable=False)
    location = Column(String(30), index=True, nullable=False)
    salary_range = Column(String(50), index=True, nullable=False)
    post_date = Column(String(50), nullable=False)
    required_skills = Column(String(500), index=True)
    deadline = Column(String(20), index=True)
    externalUrl = Column(String(50), index=True, nullable=False)
    is_featured = Column(Boolean, default=False)


# The incoming data schema; for validating inputs
class JobCreate(BaseModel):
    title: str = Field(..., description="Job title e.g Backend developer")
    jobType: str = Field(..., description="Type of job (e.g., Full-time, Part-time)")
    category: str = Field(..., description="Job category")
    description: str = Field(..., description="Job description")
    location: str = Field(..., description="Job location")
    salary_range: str = Field(description="salary range or salary")
    required_skills: list[str] = Field(description="Job required_skills")
    deadline: str = Field(description="Application deadline")
    externalUrl: Optional[str] = None

# The outgoing response schema; what is sent back to the user
class JobResponse(BaseModel):
    title: str
    jobType: str
    category: str
    description: int
    location: str
    salary_range: str
    post_date: str
    required_skills: list[str]
    deadline: str

    class Config:
        from_attributes = True
