# tests/conftest.py
import os, sys, asyncio
import pytest
from httpx import AsyncClient, ASGITransport

# プロジェクトルート（conftest.py の1つ上の階層）
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    from main import app
except ModuleNotFoundError:
    # もし main.py が mini_mathway_fastapi/ 配下ならこっち
    from mini_mathway_fastapi.main import app

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


