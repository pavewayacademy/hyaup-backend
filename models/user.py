from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    """ Represents the structure of user in the database"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: EmailStr = Field(index=True)
    phone_number: str
    role: str = Field(default="user")
    

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
