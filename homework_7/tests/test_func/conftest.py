import asyncio

import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine

from homework_7.db.models.models import Base
from homework_7.main import app


@pytest_asyncio.fixture(scope="function")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def setup_database():
    BASE_URL = "sqlite+aiosqlite:///./student.db"
    engine = create_async_engine(BASE_URL)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
def app_client(setup_database):
    with TestClient(app) as client:
        yield client
