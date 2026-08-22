from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from config.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    age = Column(Integer)
    email = Column(String(100), unique=True, index=True)
    role = Column(String(50))
    first_name = Column(String(100))
    last_name = Column(String(100))
    gender = Column(String(10))
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    last_login_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class UserBase(BaseModel):
    age: int = Field(..., description="Age of the user", ge=17, lt=120)
    email: EmailStr = Field(description="User email address")
    role: str = Field(description="User role")
    first_name: str = Field(description="User first name", min_length=1, max_length=50)
    last_name: str = Field(description="User last name", min_length=1, max_length=50)
    gender: str = Field(description="User gender")

    class Config:
        from_attributes = True

class CreateUser(UserBase):
    password: str = Field(description="User password", min_length=8, max_length=64)

class UserResponse(UserBase):
    id: int
    username: str
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password", min_length=8, max_length=64)
    