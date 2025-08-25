Mini Mathway FastAPI

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

# 2. (Optional) create a virtual environment
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
uvicorn main:app --reload
# → Open http://127.0.0.1:8000/ and http://127.0.0.1:8000/docs
