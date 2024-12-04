from sqlalchemy import select, insert, and_
from app.database import async_session_maker


# DAO - Data Access Object; Services; Patterns; Repository
class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            results = await session.execute(query)
            result = results.mappings().one_or_none()
            return [result] if result else []

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            results = await session.execute(query)
            result = results.mappings().one_or_none()
            return [result] if result else []

    @classmethod
    async def find_all(cls, **filter_by):   # or filter_by=None - but you can't use filters
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns)
            # Додаємо умови, якщо є фільтри
            if filter_by:
                filters = [getattr(cls.model, key) == value for key, value in filter_by.items()]
                query = query.where(and_(*filters))
            results = await session.execute(query)
            # print(f'Find All = {results}')
            return results.mappings().all()

    @classmethod
    async def add(cls, **data):  # or filter_by=None - but you can't use filters
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

