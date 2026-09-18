from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlmodel import Field, SQLModel

class Company(SQLModel, table=True):
    """ Represents the structure of a company in the database"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    name: str = Field(index=True)
    industry: str
    city: str
    email: Optional[EmailStr] = Field(default=None, index=True, unique=True)
    size: Optional[str] = None
    website: Optional[str] = None
    bio: Optional[str] = None
    logo: Optional[str] = None
    phone: Optional[str] = Field(default=None, index=True, unique=True)

class NewCompany(BaseModel):
    company_name: str
    industry: str
    city: str
    user_id: int
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company_size: Optional[str] = None
    website: Optional[str] = None
    bio: Optional[str] = None
    logo: Optional[str] = None