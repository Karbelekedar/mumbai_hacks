# app/schemas/bulk_request.py
from pydantic import BaseModel
from typing import List, Optional

class LocationQuery(BaseModel):
    q: str
    custom_id: Optional[str] = None

class BulkWeatherRequest(BaseModel):
    locations: List[LocationQuery]