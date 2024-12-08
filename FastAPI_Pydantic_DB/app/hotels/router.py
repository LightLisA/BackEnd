import asyncio
from datetime import date, datetime
from fastapi import APIRouter, Depends, Query
from app.hotels.schemas import SHotel, SHotelInfo
from app.hotels.services_dao import HotelsDAO
from pydantic import parse_obj_as
from fastapi_cache.decorator import cache


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)


@router.get("")
async def get_all_hotels() -> list[SHotel]:
    return await HotelsDAO.find_all()


@router.get("/{location}")
@cache(expire=40)
async def get_hotels_by_name(
        # location: HotelList = Depends()
        location: str,
        date_from: date = Query(..., description=f"Example, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Example, {datetime.now().date()}"),
):
    await asyncio.sleep(3)
    hotels = await HotelsDAO.get_list_of_hotels(location, date_from, date_to)
    print(f"HOTEL === {hotels}")
    hotels_json = parse_obj_as(list[SHotelInfo], hotels)
    print(hotels_json)
    return hotels_json


@router.get("/id/{hotel_id}")
async def get_hotel_info_by_id(hotel_id: int) -> list[SHotel]:
    return await HotelsDAO.find_all(id=hotel_id)
