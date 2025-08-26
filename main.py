from fastapi import FastAPI, HTTPException, Request
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations,
    convert_xor, implicit_multiplication_application
)

app = FastAPI(title="Mini Mathway API")

# ^ を累乗として解釈 + 2x → 2*x のような暗黙の掛け算を許可
TRANSFORMS = standard_transformations + (
    convert_xor,
    implicit_multiplication_application,
)

def parse_math(expr: str):
    """数式文字列を安全にパース"""
    try:
        return parse_expr(str(expr), transformations=TRANSFORMS)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Parse error: {e}")

# -----------------------
# Endpoints
# -----------------------

@app.get("/")
def root():
    return {"message": "Welcome to Mini Mathway API"}

@app.get("/ping")
def ping():
    return {"ok": True}

@app.post("/simplify")
async def simplify(request: Request):
    data = await request.json()
    expr_s = data.get("expr")
    if not expr_s:
        raise HTTPException(status_code=400, detail="Missing 'expr'")
    expr = parse_math(expr_s)
    res = sp.simplify(expr)
    return {"input": expr_s, "result": str(res)}

@app.post("/factor")
async def factor(request: Request):
    data = await request.json()
    expr_s = data.get("expr")
    if not expr_s:
        raise HTTPException(status_code=400, detail="Missing 'expr'")
    expr = parse_math(expr_s)
    res = sp.factor(expr)
    return {"input": expr_s, "result": str(res)}

@app.post("/evaluate")
async def evaluate(request: Request):
    data = await request.json()
    expr_s = data.get("expr")
    values = data.get("values", {})
    if not expr_s:
        raise HTTPException(status_code=400, detail="Missing 'expr'")
    expr = parse_math(expr_s)
    res = expr.evalf(subs=values)
    return {"input": expr_s, "result": str(res)}

@app.post("/solve")
async def solve(request: Request):
    data = await request.json()
    expr_s = data.get("expr")
    var_s = data.get("var", "x")
    if not expr_s:
        raise HTTPException(status_code=400, detail="Missing 'expr'")
    expr = parse_math(expr_s)
    var = sp.symbols(var_s)
    roots = sp.solve(expr, var)
    return {"input": expr_s, "solutions": [str(r) for r in roots]}

@app.post("/derivative")
async def derivative(request: Request):
    data = await request.json()
    expr_s = data.get("expr")
    var_s = data.get("var", "x")
    order = int(data.get("order", 1))
    if not expr_s:
        raise HTTPException(status_code=400, detail="Missing 'expr'")
    expr = parse_math(expr_s)
    var = sp.symbols(var_s)
    res = sp.diff(expr, var, order)
    return {"input": expr_s, "var": var_s, "order": order, "result": str(res)}

@app.post("/integral")
async def integral(request: Request):
    data = await request.json()
    expr_s = data.get("expr")
    var_s = data.get("var", "x")
    if not expr_s:
        raise HTTPException(status_code=400, detail="Missing 'expr'")
    expr = parse_math(expr_s)
    var = sp.symbols(var_s)
    res = sp.integrate(expr, var)
    return {"input": expr_s, "result": str(res)}

@app.post("/limit")
async def limit(request: Request):
    data = await request.json()
    expr_s = data.get("expr")
    var_s = data.get("var", "x")
    point = data.get("point", 0)
    if not expr_s:
        raise HTTPException(status_code=400, detail="Missing 'expr'")
    expr = parse_math(expr_s)
    var = sp.symbols(var_s)
    res = sp.limit(expr, var, point)
    return {"input": expr_s, "result": str(res)}

@app.post("/matrix/rref")
async def matrix_rref(request: Request):
    data = await request.json()
    mat = data.get("matrix")
    if not mat:
        raise HTTPException(status_code=400, detail="Missing 'matrix'")
    try:
        M = sp.Matrix(mat)
        rrefM, pivots = M.rref()
        return {
            "input": mat,
            "rref": [list(map(int, row)) for row in rrefM.tolist()],
            "pivots": list(map(int, pivots)),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"RREF failed: {e}")
