from typing import Optional
from pydantic import BaseModel, Field
from datetime import date


class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list[str]
    quantity: int
    image_id: int
    total_cost:  int = Field(..., alias="total_cost")
    rooms_left:  int = Field(..., alias="rooms_left")

    class Config:
        from_attributes = True
