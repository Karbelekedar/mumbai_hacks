# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserSignup(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, pattern=r"^\d{10}$")
    password: str

class UserLogin(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, pattern=r"^\d{10}$")
    password: str