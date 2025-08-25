from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, Knight! FastAPI is working 🎉"}

@app.get("/ping")
def ping():
    return {"ok": True}

@app.get("/double/{number}")
def double_number(number: int):
    return {"result": number * 2}

# ルート一覧を確認できるデバッグ用
@app.get("/routes")
def list_routes():
    return [r.path for r in app.router.routes]
