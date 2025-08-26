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

# --- /evaluate ---------------------------------------------------------------
@app.post("/evaluate")
async def evaluate(request: Request):
    data = await request.json()
    expr_str = data.get("expr")
    if not expr_str:
        raise HTTPException(status_code=400, detail="Missing 'expr'")

    # 変数辞書（expr 以外のキーを全部使う）
    var_values = {k: v for k, v in data.items() if k != "expr"}

    try:
        expr = parse_expr(expr_str)
        # 代入 → 数値化
        subsd = expr.subs({sp.Symbol(k): v for k, v in var_values.items()})
        # SymPy型をPythonの数値へ
        res = sp.N(subsd)
        # 可能なら int に（14.0 → 14）
        if res.is_integer():
            res = int(res)
        else:
            res = float(res)
        return {"input": expr_str, "result": res}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Evaluate failed: {e}")

# --- /solve ------------------------------------------------------------------
@app.post("/solve")
async def solve(request: Request):
    data = await request.json()
    expr_str = data.get("expr")
    var_name = data.get("var")
    if not expr_str or not var_name:
        raise HTTPException(status_code=400, detail="Missing 'expr' or 'var'")

    try:
        expr = parse_expr(expr_str)
        var = sp.Symbol(var_name)
        sols = sp.solve(expr, var)
        # テストは文字列のリストを期待
        return {"input": expr_str, "result": [str(s) for s in sols]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Solve failed: {e}")

# --- /matrix/rref ------------------------------------------------------------
@app.post("/matrix/rref")
async def matrix_rref(request: Request):
    data = await request.json()
    mat = data.get("matrix")
    if not mat:
        raise HTTPException(status_code=400, detail="Missing 'matrix'")

    try:
        M = sp.Matrix(mat)
        rrefM, pivots = M.rref()
        # 文字列にせず、そのままPythonのリストで返す
        return {
            "input": mat,
            "rref": rrefM.tolist(),
            "pivots": list(pivots),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"RREF failed: {e}")
