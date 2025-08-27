import pytest

@pytest.mark.asyncio
async def test_simplify(client):
    res = await client.post("/simplify", json={"expression": "2*x + 3*x"})
    assert res.status_code == 200, res.text
    body = res.json()
    assert body.get("result") in ("5*x", "5*x")



