from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    """ Represents the structure of user in the database"""
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: str = Field(index=True)
    email: EmailStr = Field(index=True)
    name: Optional[str] = None
    phone_number: Optional[str] = None
    profile_picture: Optional[str] = None
    role: str = Field(default="user")
    is_onboarded: Optional[bool] = False
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    

class FirebaseUser(BaseModel):
    email: EmailStr
    display_name: Optional[str] = None
    photo_url: Optional[str] = None
    phone_number: Optional[str] = None
    email_verified: Optional[bool] = False
    disabled: Optional[bool] = False

class CreateFirebaseUser(BaseModel):
    email: EmailStr
    password: str
    display_name: Optional[str] = None
    photo_url: Optional[str] = None
    phone_number: Optional[str] = None

class UpdateFirebaseUser(BaseModel):
    display_name: Optional[str] = None
    photo_url: Optional[str] = None
    phone_number: Optional[str] = None

class UserOnboardingData(BaseModel):
    company_name: Optional[str] = None
    industry: Optional[str] = None
    city: Optional[str] = None
    company_size: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    bio: Optional[str] = None

class UpdateUserAccount(BaseModel):
    uid: str
    email: EmailStr
    role: str
    name: Optional[str] = None
    is_onboarded: Optional[bool] = False
    company_name: Optional[str] = None
    industry: Optional[str] = None
    city: Optional[str] = None
    company_size: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None

