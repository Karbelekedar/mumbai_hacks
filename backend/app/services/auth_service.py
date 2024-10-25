# app/services/auth_service.py
from app.db.mongodb import db
from app.utils.hashing import hash_password, verify_password
from app.schemas.user import UserSignup, UserLogin
from app.models.user import User

users_collection = db["users"]

def signup_user(user_data: UserSignup) -> str:
    if users_collection.find_one({"email": user_data.email}) or users_collection.find_one({"phone_number": user_data.phone_number}):
        return "User already exists"

    user_data.password = hash_password(user_data.password)
    user = User(**user_data.dict())
    users_collection.insert_one(user.dict())
    return "User created successfully"

def login_user(login_data: UserLogin) -> str:
    user = users_collection.find_one({
        "$or": [{"email": login_data.email}, {"phone_number": login_data.phone_number}]
    })

    if not user or not verify_password(login_data.password, user["password"]):
        return "Invalid credentials"

    return "Login successful"