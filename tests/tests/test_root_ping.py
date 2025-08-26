# tests/test_root_ping.py
import pytest

@pytest.mark.asyncio
async def test_root(client):
    r = await client.get("/")
    assert r.status_code == 200
    assert "message" in r.json()

@pytest.mark.asyncio
async def test_ping(client):
    r = await client.get("/ping")
    assert r.status_code == 200
    assert r.json() == {"ok": True}
