from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings

DATABASE_URL = settings.database_url

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal as db:
        try:
            yield db  
        finally:
            await db.close() 