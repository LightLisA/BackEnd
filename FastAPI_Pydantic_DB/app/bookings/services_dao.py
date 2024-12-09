from datetime import date
from app.database import async_session_maker
from sqlalchemy import select, func, and_, or_, insert, delete, inspect
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.services_dao_repository.base import BaseDAO


# DAO - Data Access Object; Services; Patterns; Repository
class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(cls,
                  user_id: int,
                  room_id: int,
                  date_from: date,
                  date_to: date
                  ):
        async with async_session_maker() as session:
            get_rooms_left = (
                select(
                    (Rooms.quantity - func.count(Bookings.room_id)).label("rooms_left")
                )
                .select_from(Bookings)
                .join(Rooms, Rooms.id == Bookings.room_id, full=True)
                .where(
                    and_(
                        Rooms.id == room_id,
                        or_(
                            Bookings.room_id.is_(None),
                            and_(
                                Bookings.date_from > date_from,
                                Bookings.date_from < date_to
                            ),
                            and_(
                                Bookings.date_from < date_from,
                                Bookings.date_to > date_from
                            ),
                        )
                    )
                )
            ).group_by(Rooms.id, Rooms.quantity)

            rooms_left = await session.execute(get_rooms_left)
            rooms_left = rooms_left.scalar()

            if not rooms_left or rooms_left > 0:
                get_price = await session.execute(select(Rooms.price).filter_by(id=room_id))
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=get_price.scalar(),
                ).returning(Bookings)

                new_booking = await session.execute(add_booking)
                await session.commit()
                result = new_booking.scalar()
                return result
            else:
                return None

    @classmethod
    async def get_list_of_bookings_by_user(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(
                    Bookings.id,
                    Bookings.room_id,
                    Bookings.user_id,
                    Bookings.date_from,
                    Bookings.date_to,
                    Bookings.price,
                    Bookings.total_cost,
                    Bookings.total_days,
                    Rooms.image_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.services
                )
                .select_from(Rooms)
                .join(Bookings, Bookings.room_id == Rooms.id, isouter=True)
                .where(
                    Bookings.user_id == user_id
                )
            )

            results = await session.execute(query)
            booked_rooms_by_user = results.mappings().all()
            print(f"Mappings All = {booked_rooms_by_user}")
            return booked_rooms_by_user

    @classmethod
    async def remove_booking_by_user(cls, user_id: int, booking_id):
        async with async_session_maker() as session:
            select_query = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.user_id == user_id,
                        Bookings.id == booking_id
                    )
                )
            )

            sel_result = await session.execute(select_query)
            booked_rooms = sel_result.scalar()
            # print(f"Booked roms = {booked_rooms}")

            if booked_rooms is not None:
                query = (
                    delete(Bookings)
                    .where(
                        and_(
                            Bookings.user_id == user_id,
                            Bookings.id == booking_id
                        )
                    )
                )
                results = await session.execute(query)
                await session.commit()
                # remove_booking = results.mappings().all()
                # print(f"Mappings All = {remove_booking}")
                return True
            else:
                return False
