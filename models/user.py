from typing import Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int = Field()
    age: int
    email: str
    role: str
    first_name: str
    last_name: str
    gender: str
    passowrd: str

class CreateUser(BaseModel):
    age: int = Field(..., description="Age of the user", ge=17, lt=120)
    email: str = Field(description="User email address")
    role: str = Field(description="User role")
    first_name: str = Field(description="User first name", min_length=1, max_length=50)
    last_name: str = Field(description="User last name", min_length=1, max_length=50)
    gender: str = Field(description="User gender")
    password: str = Field(description="User password", min_length=8, max_length=64)
    password_hash: Optional[str] = None

