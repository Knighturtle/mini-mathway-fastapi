# tests/test_api.py
import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from main import app

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/")
    assert r.status_code == 200
    assert "message" in r.json()

@pytest.mark.asyncio
async def test_ping():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/ping")
    assert r.status_code == 200
    assert r.json() == {"ok": True}

# ---- algebra / calculus ----

@pytest.mark.asyncio
async def test_simplify_ok():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post("/simplify", json={"expr": "2*x + 3*x"})
    assert r.status_code == 200
    assert r.json()["result"] == "5*x"

@pytest.mark.asyncio
async def test_simplify_bad_request():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post("/simplify", json={"expr": "???bad"})
    assert r.status_code == 400

@pytest.mark.asyncio
async def test_factor():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post("/factor", json={"expr": "x**2 - 1"})
    assert r.status_code == 200
    assert r.json()["result"] in {"(x - 1)*(x + 1)", "(x + 1)*(x - 1)"}  # 出力順の差を許容

@pytest.mark.asyncio
async def test_evaluate():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post("/evaluate", json={"expr": "x**2 + y", "subs": {"x": 3, "y": 5}})
    assert r.status_code == 200
    assert r.json()["result"] == "14"

@pytest.mark.asyncio
async def test_solve():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post("/solve", json={"expr": "Eq(x + 2, 5)", "var": "x"})
    assert r.status_code == 200
    assert r.json()["result"] == "[3]"

@pytest.mark.asyncio
async def test_derivative():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post("/derivative", json={"expr": "x**3", "var": "x", "order": 2})
    assert r.status_code == 200
    assert r.json()["result"] == "6*x"

@pytest.mark.asyncio
async def test_integral():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post("/integral", json={"expr": "2*x", "var": "x"})
    assert r.status_code == 200
    # 不定積分なので +C は出ない想定。Sympyの表現差を吸収
    assert r.json()["result"] in {"x**2", "x**2"}  # 将来表現が変わっても通るように

@pytest.mark.asyncio
async def test_limit():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post("/limit", json={"expr": "sin(x)/x", "var": "x", "to": "0"})
    assert r.status_code == 200
    assert r.json()["result"] == "1"

# ---- linear algebra ----

@pytest.mark.asyncio
async def test_matrix_rref():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post("/matrix/rref", json={"matrix": [[1, 2], [3, 4]]})
    assert r.status_code == 200
    body = r.json()
    assert "rref" in body and "pivots" in body
    # RREF の一例: [[1, 0], [0, 1]]
    assert body["rref"] == "[[1, 0], [0, 1]]"
