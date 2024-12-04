# from app.hotels.router import router
from fastapi import Depends, APIRouter
from app.hotels.rooms.schemas import RoomsListOfHotel, SRoom
from app.hotels.rooms.services_dao import RoomsDAO
from app.hotels.rooms.services_dao import Rooms


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)


@router.get("/{hotel_id}/rooms")
async def get_all_rooms_for_hotel(data_filter: RoomsListOfHotel = Depends()) -> list[SRoom]:
    rooms = await RoomsDAO.get_rooms_by_hotel_id(data_filter)
    return [
        SRoom(
            **room['Rooms'].__dict__,
            rooms_left=room['rooms_left'],
            total_cost=room['total_cost']
        )
        for room in rooms
    ]
