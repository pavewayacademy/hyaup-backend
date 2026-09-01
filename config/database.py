from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
# pyrefly: ignore [missing-import]
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from config.config import settings

# Create the async engine
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# Initialize the Database
async def init_db():
    """ Create all the database tables defined via SQLModl"""
    async with engine.begin() as conn:
        # Run sync table generation in an async execution context
        await conn.run_sync(SQLModel.metadata.create_all)

# Get async session factory
async def get_session() -> AsyncSession:
    """ Dependency provider yielding an asynchronous database session."""
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session