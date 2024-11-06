from fastapi import FastAPI, Query, Depends
from typing import Optional
from datetime import date
from pydantic import BaseModel


app = FastAPI()


class HotelSearchArg:
    def __init__(self,
                 location: str,
                 date_from: date,
                 date_to: date,
                 has_spa: Optional[bool] = None,
                 stars: Optional[int] = Query(None, ge=1, le=5),
                 ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.has_spa = has_spa
        self.stars = stars


class SchemaHotel(BaseModel):
    address: str
    name: str
    stars: int


# @app.get("/hotels", response_model=list[SHotel])
@app.get("/hotels")
def get_hotels(serch_args: HotelSearchArg = Depends()) -> list[SchemaHotel]:
    hotels = [
        {
            "address": "st. NewBon 44",
            "name": "Verona",
            "stars": 5
        },
        {
            "address": "st. NewBon 48",
            "name": "Baton",
            "stars": 3
        },
    ]
    return hotels


class SchemaBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post("/booking")
def add_booking(booking: SchemaBooking):
    pass
