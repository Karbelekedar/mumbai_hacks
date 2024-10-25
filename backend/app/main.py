# app/main.py
from fastapi import FastAPI
from app.routes import auth_routes, weather_routes

app = FastAPI()

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(weather_routes.router, prefix="/api/weather", tags=["Weather"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Weather and Auth API Service"}