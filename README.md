# Mini Mathway FastAPI

[![Run Tests](https://github.com/Knighturtle/mini-mathway-fastapi/actions/workflows/test.yml/badge.svg)](https://github.com/Knighturtle/mini-mathway-fastapi/actions/workflows/test.yml)

A FastAPI-based math API inspired by Mathway.
This project provides endpoints to simplify expressions, factorize polynomials, solve equations, compute derivatives, integrals, limits, and perform matrix operations using SymPy
.

- **Language**: Python 3.13  
- **Main Libraries**: FastAPI, Uvicorn, SymPy, Pydantic  
- **API Docs**: After running → `http://127.0.0.1:8000/docs`

---

## Table of Contents

- [Quickstart](#quickstart)
- [Available Endpoints](#available-endpoints)
- [Examples](#examples)
- [Usage (curl / Python / HTTPie)](#usage-curl--python--httpie)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Roadmap](#roadmap)
- [License](#license)

---

## Quickstart

```bash
# 1. Clone
git clone https://github.com/Knighturtle/mini-mathway-fastapi.git
cd mini-mathway-fastapi

# 2. (Optional) Create virtual environment
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.\.venv\Scripts\activate    # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
uvicorn main:app --reload
# Open http://127.0.0.1:8000/docs

http POST http://127.0.0.1:8000/simplify expr="2*x + 3*x"

{
  "input": "2*x + 3*x",
  "result": "5*x"
}

pytest -q
