from typing import Optional
from pydantic import BaseModel
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
    total_cost: int
    rooms_left: Optional[int] = None

    class Config:
        from_attributes = True


class RoomsListOfHotel(BaseModel):
    hotel_id: int
    date_from: date
    date_to: date
