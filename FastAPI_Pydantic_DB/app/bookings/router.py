from fastapi import APIRouter, Depends
from app.bookings.schemas import SBooking
from app.bookings.services_dao import BookingDAO
from app.users.models import Users
from app.users.dependecies import get_current_user



router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)):    # -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user[0].id)
