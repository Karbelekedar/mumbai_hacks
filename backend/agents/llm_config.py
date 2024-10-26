import os
from dotenv import load_dotenv

load_dotenv()

# Configuration for the Market Analyst Agent
config_list_market = [{
    "model" : "gpt-4o",
    "temperature" : "0.9",
    "api_key": os.getenv("AUTOGEN_MODEL_API_KEY")
}]

