from datetime import date
from app.database import async_session_maker
from sqlalchemy import select, func, and_, or_, insert, delete
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.services_dao_repository.base import BaseDAO


# DAO - Data Access Object; Services; Patterns; Repository
class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            booked_rooms = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.room_id == room_id,
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_from <= date_to
                            ),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to > date_from
                            ),
                        )
                    )
                ).cte("booked_rooms")  # Common Table Expression (WITH)
            )

            get_rooms_left_query = (
                select(
                    (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
                )
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, booked_rooms.c.room_id)
            )

            # print(get_rooms_left_query.compile(engine, compile_kwargs={"literal_binds": True}))
            result = await session.execute(get_rooms_left_query)
            rooms_left = result.scalar()
            # print(f"Rooms left: {rooms_left}")

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                ).returning(Bookings)

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
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
