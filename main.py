from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Any
import sympy as sp

app = FastAPI(title="Mini Mathway API")

# 使える記号・関数を制限（安全のため eval は使わない）
x, y, z, a, b = sp.symbols("x y z a b")
SAFE_ENV = {
    "x": x, "y": y, "z": z, "a": a, "b": b,
    # 基本関数
    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
    "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
    "sinh": sp.sinh, "cosh": sp.cosh, "tanh": sp.tanh,
    "exp": sp.exp, "log": sp.log, "ln": sp.log, "sqrt": sp.sqrt,
    "pi": sp.pi, "E": sp.E,
    "Abs": sp.Abs,
}

def parse_expr(expr: str) -> sp.Expr:
    try:
        # sympify で安全にパース（許可した名前だけ解釈）
        return sp.sympify(expr, locals=SAFE_ENV, evaluate=True)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid expression: {e}")

def parse_symbol(name: str) -> sp.Symbol:
    if name not in SAFE_ENV or not isinstance(SAFE_ENV[name], sp.Symbol):
        raise HTTPException(status_code=400, detail=f"Unsupported variable: {name}")
    return SAFE_ENV[name]

def to_str(obj: Any) -> Any:
    # JSON 化のために SymPy オブジェクトを文字列へ
    if isinstance(obj, (sp.Basic, sp.MatrixBase)):
        return str(obj)
    if isinstance(obj, (list, tuple)):
        return [to_str(o) for o in obj]
    if isinstance(obj, dict):
        return {k: to_str(v) for k, v in obj.items()}
    return obj

# ---------- Pydantic モデル ----------
class ExprIn(BaseModel):
    expr: str = Field(..., examples=["x^2 + 2*x + 1"])

class EvaluateIn(BaseModel):
    expr: str = Field(..., examples=["x^2 + 2*x + 1"])
    var: str = Field("x", examples=["x"])
    value: float = Field(..., examples=[3])

class SolveIn(BaseModel):
    eq: str = Field(..., examples=["x^2 - 4"])
    var: str = Field("x", examples=["x"])

class DiffIntIn(BaseModel):
    expr: str = Field(..., examples=["sin(x)*x^2"])
    var: str = Field("x", examples=["x"])
    order: int = Field(1, ge=1, le=5, examples=[1])

class LimitIn(BaseModel):
    expr: str = Field(..., examples=["(sin(x))/x"])
    var: str = Field("x", examples=["x"])
    to: float | str = Field(0, examples=[0])   # "oo" や "-oo" も可
    dir: str = Field("+", pattern=r"^[\+\-]$") # 片側極限: '+' or '-'

class MatrixIn(BaseModel):
    matrix: List[List[float]]

# ---------- ルート ----------
@app.get("/")
def root():
    return {"message": "Mini Mathway API (FastAPI + SymPy)"}

@app.get("/ping")
def ping():
    return {"ok": True}

@app.post("/simplify")
def simplify(inp: ExprIn):
    expr = parse_expr(inp.expr)
    return {"input": inp.expr, "result": to_str(sp.simplify(expr))}

@app.post("/factor")
def factor(inp: ExprIn):
    expr = parse_expr(inp.expr)
    return {"input": inp.expr, "result": to_str(sp.factor(expr))}

@app.post("/evaluate")
def evaluate(inp: EvaluateIn):
    expr = parse_expr(inp.expr)
    var = parse_symbol(inp.var)
    try:
        val = sp.N(expr.subs(var, inp.value))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Evaluate failed: {e}")
    return {"input": inp.expr, "var": inp.var, "value": inp.value, "result": to_str(val)}

@app.post("/solve")
def solve(inp: SolveIn):
    var = parse_symbol(inp.var)
    eq = parse_expr(inp.eq)
    # eq = 0 の解を返す
    try:
        sols = sp.solve(sp.Eq(eq, 0), var)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Solve failed: {e}")
    return {"equation": f"{inp.eq}=0", "var": inp.var, "solutions": to_str(sols)}

@app.post("/derivative")
def derivative(inp: DiffIntIn):
    expr = parse_expr(inp.expr)
    var = parse_symbol(inp.var)
    try:
        res = sp.diff(expr, var, inp.order)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Differentiate failed: {e}")
    return {"input": inp.expr, "var": inp.var, "order": inp.order, "result": to_str(res)}

@app.post("/integral")
def integral(inp: DiffIntIn):
    expr = parse_expr(inp.expr)
    var = parse_symbol(inp.var)
    try:
        res = sp.integrate(expr, var)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Integrate failed: {e}")
    return {"input": inp.expr, "var": inp.var, "result": to_str(res)}

@app.post("/limit")
def limit(inp: LimitIn):
    expr = parse_expr(inp.expr)
    var = parse_symbol(inp.var)
    to = sp.oo if inp.to == "oo" else -sp.oo if inp.to == "-oo" else inp.to
    try:
        res = sp.limit(expr, var, to, dir=inp.dir)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Limit failed: {e}")
    return {"input": inp.expr, "var": inp.var, "to": inp.to, "dir": inp.dir, "result": to_str(res)}

@app.post("/matrix/rref")
def matrix_rref(inp: MatrixIn):
    try:
        M = sp.Matrix(inp.matrix)
        rrefM, pivots = M.rref()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"RREF failed: {e}")
    return {"input": inp.matrix, "rref": to_str(rrefM), "pivots": pivots}
