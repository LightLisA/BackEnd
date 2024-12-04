from pydantic import BaseModel
from typing import Optional
from datetime import date
from fastapi import Query


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int
    rooms_left: Optional[int] = None

    class Config:
        from_attributes = True
        from_orm = True


class HotelList(BaseModel):
    location: str
    date_from: date
    date_to: date


class HotelID(BaseModel):
    hotel_id: int


"""
class HotelSearchArg:
    def __init__(self,
                 location: str,
                 date_from: date,
                 date_to: date,
                 wi_fi: Optional[bool] = None,
                 swimming_pool: Optional[bool] = None,
                 parking: Optional[bool] = None,
                 air_conditioning_in_the_room: Optional[bool] = None,
                 gym: Optional[bool] = None,
                 stars: Optional[int] = Query(None, ge=1, le=5),
                 ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.wi_fi = wi_fi
        self.swimming_pool = swimming_pool
        self.parking = parking
        self.air_conditioning_in_the_room = air_conditioning_in_the_room
        self.gym = gym
        self.stars = stars
"""
