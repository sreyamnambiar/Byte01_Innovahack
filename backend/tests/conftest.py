"""
DarkTrust – Pytest Configuration

Sets up the async test client and overrides the database dependency 
so unit tests do not mutate the production database.
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.main import application
from app.database.session import get_db
from app.database.base import Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=None
)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Creates a fresh in-memory database for each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with TestingSessionLocal() as session:
        yield session
        
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def async_client(db_session: AsyncSession):
    """Provides a FastAPI AsyncClient with the database dependency overridden."""
    def override_get_db():
        yield db_session
        
    application.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(
        transport=ASGITransport(app=application), 
        base_url="http://test"
    ) as client:
        yield client
        
    application.dependency_overrides.clear()
