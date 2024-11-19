from sqlalchemy import select
from app.bookings.models import Bookings
from app.database import async_session_maker


# DAO - Data Access Object; Services; Patterns; Repository
class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            results = await session.execute(query)
            return results.mappings().one_or_none()

    @classmethod
    async def find_one_or_none(cls, filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            results = await session.execute(query)
            return results.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            results = await session.execute(query)
            return results.mappings().all()
