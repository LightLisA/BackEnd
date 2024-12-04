from sqlalchemy import select, func, and_, or_
from app.services_dao_repository.base import BaseDAO
from app.hotels.models import Hotels
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.database import async_session_maker


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def get_list_of_hotels(cls, values):
        async with async_session_maker() as session:
            # values => location='Алтай' date_from=None date_to=None
            if values.date_from is None and values.date_to is None:
                query = select(Hotels).where(Hotels.location.ilike(f'%{values.location}%'))
            else:
                count_booked_rooms_by_hotels = (
                    select(
                        Rooms.hotel_id,
                        (func.count(Bookings.room_id)).label("total_booked_rooms")
                    )
                    .select_from(Bookings)
                    .join(Rooms, Rooms.id == Bookings.room_id)
                    .where(
                        or_(
                            and_(
                                Bookings.date_from >= values.date_from,
                                Bookings.date_from <= values.date_to,
                            ),
                            and_(
                                Bookings.date_from <= values.date_from,
                                Bookings.date_to > values.date_from,
                            ),
                        )
                    )
                    .group_by(Rooms.hotel_id)
                    .cte("count_booked_rooms_by_hotels")
                )

                query = (
                    select(
                        Hotels,
                        (Hotels.rooms_quantity - func.coalesce(count_booked_rooms_by_hotels.c.total_booked_rooms, 0)).label("rooms_left")
                    )
                    .select_from(count_booked_rooms_by_hotels)
                    .join(Hotels, Hotels.id == count_booked_rooms_by_hotels.c.hotel_id, isouter=True)
                    .where((Hotels.rooms_quantity - func.coalesce(count_booked_rooms_by_hotels.c.total_booked_rooms,
                                                                  0)) > 0)  # Перевірка наявності вільних номерів
                    .where(Hotels.location.ilike(f'%{values.location}%'))
                )

            results = await session.execute(query)
            # hotels = results.scalars().all()
            # print(f"Scalars All = {hotels}")
            hotels = results.mappings().all()
            print(f"Mappings All = {hotels}")
            return hotels

