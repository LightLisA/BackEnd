from fastapi import APIRouter, Depends
from app.bookings.schemas import SBooking, BookingsID
from app.bookings.services_dao import BookingDAO
from app.users.models import Users
from app.users.dependecies import get_current_user
from datetime import date
from app.exeptions import *


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.get_list_of_bookings_by_user(user_id=user[0].id)


@router.post("")
async def add_booking(
        room_id: int,
        date_from: date,
        date_to: date,
        user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user[0].id, room_id, date_from, date_to)
    if not booking:
        raise HTTPException_RoomCannotBeBooked


@router.delete("/{booking_id}")
async def delete_booking(
        booking_id: BookingsID = Depends(),
        user: Users = Depends(get_current_user)
):
    remove_booking = await BookingDAO.remove_booking_by_user(user[0].id, booking_id.booking_id)
    if remove_booking:
        return {"status": "Booking deleted successfully"}
    else:
        raise HTTPException_BookedRoomHasRemoved
