from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config import settings


# створюємо двіжок
engine = create_async_engine(settings.DATABASE_URL)

# генератор сесій - транзакцій
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base (DeclarativeBase):
    pass
