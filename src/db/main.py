from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import SQLModel, create_engine
from src.books.models import Book
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker


engine = AsyncEngine(create_engine(url=Config.DATABASE_URL, echo=True))


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with Session() as session:
        yield session
