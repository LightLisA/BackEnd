from app.hotels.rooms.models import Rooms
from sqlalchemy import select, func, and_, or_
from app.services_dao_repository.base import BaseDAO
from app.hotels.models import Hotels
from app.bookings.models import Bookings
from app.database import async_session_maker


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_rooms_by_hotel_id(cls, hotel_id, date_from, date_to):
        async with async_session_maker() as session:
            count_booked_rooms_by_hotels = (
                select(
                    Rooms.id,
                    Rooms.hotel_id,
                    (func.count(Bookings.room_id)).label("total_booked_rooms")
                )
                .select_from(Bookings)
                .join(Rooms, Rooms.id == Bookings.room_id)
                .where(
                    and_(
                        Rooms.hotel_id == hotel_id,
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
                )
                .group_by(Rooms.id)
                .cte("count_booked_rooms_by_hotels")
            )

            query = (
                select(
                    Rooms.__table__.columns,
                    ((date_to - date_from).days * Rooms.price).label("total_cost"),
                    (Rooms.quantity - func.coalesce(count_booked_rooms_by_hotels.c.total_booked_rooms, 0))
                    .label("rooms_left")
                )
                .select_from(count_booked_rooms_by_hotels)
                .join(Rooms, Rooms.id == count_booked_rooms_by_hotels.c.id)
                .join(Hotels, Hotels.id == count_booked_rooms_by_hotels.c.hotel_id, isouter=True)
            )

        results = await session.execute(query)
        hotels = results.all()
        print(f"Mappings All = {hotels}")
        return hotels
