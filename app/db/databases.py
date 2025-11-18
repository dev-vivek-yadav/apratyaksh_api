from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.settings import get_settings

settings = get_settings()

# Async MySQL URL example:
# mysql+aiomysql://user:password@host:port/dbname
DATABASE_URL = (
    f"mysql+aiomysql://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,               # Set True only while debugging
    pool_pre_ping=True,       # Avoid stale MySQL connections
    pool_recycle=1800,        # Refresh idle connections (30 mins)
    future=True
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=True,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession,
)

# Base for models
Base = declarative_base()

# Dependency for using DB in FastAPI routes
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
