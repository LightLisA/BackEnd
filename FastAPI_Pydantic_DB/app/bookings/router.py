from fastapi import APIRouter
from app.bookings.schemas import SBooking
from app.bookings.services_dao import BookingDAO


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.get("")
async def get_bookings() -> list[SBooking]:
    return await BookingDAO.find_all()
