from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)


def create_engine(postgres_dsn: PostgresDsn) -> AsyncEngine:
    return create_async_engine(url=postgres_dsn)

def create_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False
    )
