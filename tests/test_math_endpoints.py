# tests/test_math_endpoints.py
import pytest

@pytest.mark.asyncio
async def test_simplify(client):
    r = await client.post("/simplify", params={"expr": "2*x + 3*x"})
    assert r.status_code == 200
    assert r.json()["result"] == "5*x"

