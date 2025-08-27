# tests/conftest.py
import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from main import app   # ← main.py に app がある場合。パスが違えば修正してください

# Windows 環境で event_loop 関連エラーを防ぐため追加
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

# 非同期クライアント fixture
@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

