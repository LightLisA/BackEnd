from fastapi import APIRouter, Depends, Query, BackgroundTasks
from app.bookings.schemas import SBooking, SBookingInfo
from app.bookings.services_dao import BookingDAO
from app.users.models import Users
from app.users.dependecies import get_current_user
from datetime import date, datetime
from app.exeptions import *
from pydantic import parse_obj_as
from app.tasks.tasks import send_booking_confirmation_email, send_booking_confirmation_email_fun


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookingInfo]:
    return await BookingDAO.get_list_of_bookings_by_user(user_id=user[0].id)


@router.post("")
async def add_booking(
        room_id: int,
        date_from: date = Query(..., description=f"Example, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Example, {datetime.now().date()}"),
        user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user[0].id, room_id, date_from, date_to)
    if not booking:
        raise HTTPException_RoomCannotBeBooked
    booking_dict = parse_obj_as(SBooking, booking).dict()
    # Celery variant for sent email
    send_booking_confirmation_email.delay(booking_dict, user[0].email)
    return booking_dict


@router.post("/theSameButOnlyForBackgroundTasks")
async def add_booking_for_background_tasks(
        background_tasks: BackgroundTasks,
        room_id: int,
        date_from: date = Query(..., description=f"Example, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Example, {datetime.now().date()}"),
        user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user[0].id, room_id, date_from, date_to)
    if not booking:
        raise HTTPException_RoomCannotBeBooked
    booking_dict = parse_obj_as(SBooking, booking).dict()

    # Celery variant for sent email
    # send_booking_confirmation_email.delay(booking_dict, user[0].email)

    # Background Task variant of sent email
    background_tasks.add_task(send_booking_confirmation_email_fun, booking_dict, user[0].email)

    return booking_dict


@router.delete("/{booking_id}")
async def delete_booking(
        booking_id: int,
        user: Users = Depends(get_current_user)
):
    remove_booking = await BookingDAO.remove_booking_by_user(user[0].id, booking_id)
    if remove_booking:
        return {"status": "Booking deleted successfully"}
    else:
        raise HTTPException_BookedRoomHasRemoved
