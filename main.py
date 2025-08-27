from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sympy import sympify, simplify as sp_simplify
from sympy.core.sympify import SympifyError

app = FastAPI()

# --- always-JSON health endpoint
class Health(BaseModel):
    status: str = "ok"

@app.get("/health", response_model=Health)
async def health():
    return {"status": "ok"}

# --- /simplify: JSON in/out, deterministic
class SimplifyIn(BaseModel):
    expression: str

class SimplifyOut(BaseModel):
    result: str

@app.post("/simplify", response_model=SimplifyOut)
async def simplify_endpoint(payload: SimplifyIn):
    try:
        expr = sympify(payload.expression)
        res = sp_simplify(expr)
        return {"result": str(res)}  # dictを返す => application/json
    except (SympifyError, ValueError) as e:
        raise HTTPException(status_code=400, detail=f"invalid expression: {e}")


