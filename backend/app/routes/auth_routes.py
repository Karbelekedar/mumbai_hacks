# app/routes/auth_routes.py
from fastapi import APIRouter, HTTPException
from app.schemas.user import UserSignup, UserLogin
from app.services.auth_service import signup_user, login_user

router = APIRouter()

@router.post("/signup")
async def signup(user: UserSignup):
    result = signup_user(user)
    if result == "User already exists":
        raise HTTPException(status_code=400, detail="User with this email or phone number already exists")
    return {"message": result}

@router.post("/login")
async def login(user: UserLogin):
    result = login_user(user)
    if result == "Invalid credentials":
        raise HTTPException(status_code=401, detail="Invalid email/phone number or password")
    return {"message": result}