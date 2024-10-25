# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = "your_database_name"
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")