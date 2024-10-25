# app/models/user.py
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    name: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    password: str