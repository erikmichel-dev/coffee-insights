from typing import List
from pydantic import BaseModel

class CoffeeVarietal(BaseModel):
    name: str
    origin: str
    producer: str
    roasting_profile: str
    price: float
    notes: List[str]
    category: str
