# from app.hotels.router import router
from datetime import date, datetime
from fastapi import Depends, APIRouter, Query
from pydantic import parse_obj_as

from app.hotels.rooms.schemas import SRoom
from app.hotels.rooms.services_dao import RoomsDAO
from app.hotels.rooms.services_dao import Rooms


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)


@router.get("/{hotel_id}/rooms")
async def get_all_rooms_for_hotel(
        hotel_id: int,
        date_from: date = Query(..., description=f"Example, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Example, {datetime.now().date()}"),
):
    rooms = await RoomsDAO.get_rooms_by_hotel_id(hotel_id, date_from, date_to)

    rooms_json = parse_obj_as(list[SRoom], rooms)
    print(rooms_json)
    return rooms_json

