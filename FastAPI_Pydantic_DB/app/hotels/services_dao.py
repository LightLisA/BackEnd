from datetime import date
from sqlalchemy import select, func, and_, or_
from app.services_dao_repository.base import BaseDAO
from app.hotels.models import Hotels
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.database import async_session_maker


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def get_list_of_hotels(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:
            """count_booked_rooms_by_hotels = (
                select(
                    Rooms.hotel_id,
                    (func.count(Bookings.room_id)).label("total_booked_rooms")
                )
                .select_from(Bookings)
                .join(Rooms, Rooms.id == Bookings.room_id)
                .where(
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to,
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from,
                        ),
                    )
                )
                .group_by(Rooms.hotel_id)
                .cte("count_booked_rooms_by_hotels")
            )

            query = (
                select(
                    Hotels,
                    (Hotels.rooms_quantity - func.coalesce(count_booked_rooms_by_hotels.c.total_booked_rooms, 0))
                    .label("rooms_left")
                )
                .select_from(count_booked_rooms_by_hotels)
                .join(Hotels, Hotels.id == count_booked_rooms_by_hotels.c.hotel_id, isouter=True)
                .where((Hotels.rooms_quantity - func.coalesce(count_booked_rooms_by_hotels.c.total_booked_rooms,
                                                              0)) > 0)  # Перевірка наявності вільних номерів
                .where(Hotels.location.ilike(f'%{location}%'))
            )"""

            bookings_for_selected_date = (
                select(Bookings)
                .filter(
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from < date_to,
                        ),
                        and_(
                            Bookings.date_from < date_from,
                            Bookings.date_to > date_from,
                        ),
                    )
                )
                .subquery("filtered_bookings")
            )

            hotels_rooms_left = (
                select(
                    (Hotels.rooms_quantity - func.count(bookings_for_selected_date.c.room_id)).label("room_left"),
                    Rooms.hotel_id
                )
                .select_from(Hotels)
                .outerjoin(Rooms, Rooms.hotel_id == Hotels.id)
                .outerjoin(bookings_for_selected_date,
                           bookings_for_selected_date.c.room_id == Rooms.id)
                .where(Hotels.location.contains(location.title()))
                .group_by(Hotels.rooms_quantity, Rooms.hotel_id)
                .cte("hotels_rooms_left")
            )

            #
            get_hotels_info = (
                select(
                    Hotels.__table__.columns,       # all columns of Hotel table
                    hotels_rooms_left.c.room_left   # additional column with amount of rooms
                )
                .select_from(Hotels)
                .join(hotels_rooms_left, hotels_rooms_left.c.hotel_id == Hotels.id)
                .where(hotels_rooms_left.c.room_left > 0)
            )

            results = await session.execute(get_hotels_info)
            hotels = results.all()
            return hotels

