from app.database import async_session_maker
from sqlalchemy import select
from app.bookings.models import Bookings
from app.services_dao_repository.base import BaseDAO


# DAO - Data Access Object; Services; Patterns; Repository
class BookingDAO(BaseDAO):
    model = Bookings
