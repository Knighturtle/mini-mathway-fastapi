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

## Available Endpoints

- `GET /` → Root message
- `GET /ping` → Health check
- `POST /simplify` → Simplify algebraic expressions
- `POST /factor` → Factorize polynomials
- `POST /solve` → Solve equations
- `POST /derivative` → Compute derivatives
- `POST /integral` → Compute integrals
- `POST /limit` → Calculate limits
- `POST /matrix/rref` → Reduced Row Echelon Form

## Examples

Simplify:

```bash
http POST http://127.0.0.1:8000/simplify expr="2*x + 3*x"

{
  "input": "2*x + 3*x",
  "result": "5*x"
}


---

#### 4. Usage (curl / Python / HTTPie)
```markdown
## Usage (curl / Python / HTTPie)

# Using curl
curl -X POST http://127.0.0.1:8000/solve -H "Content-Type: application/json" -d '{"expr":"x^2-4","var":"x"}'

# Using HTTPie
http POST http://127.0.0.1:8000/solve expr="x^2-4" var="x"

# Using Python requests
import requests
r = requests.post("http://127.0.0.1:8000/solve", json={"expr":"x^2-4", "var":"x"})
print(r.json())

## Testing

Run all tests with:

```bash
pytest -q


---

## Future Work / Extensions

This project is designed to be extensible for advanced applications in AI and data science.  
Potential future directions include:

- **Integration with OCR**: Recognize handwritten or scanned mathematical expressions and process them via the API.  
- **AI-powered symbolic computation**: Use machine learning models to complement SymPy for equation solving and optimization.  
- **Mathematical tutoring assistant**: Extend the API into a conversational AI that explains step-by-step solutions.  
- **Deployment as a scalable service**: Containerization (Docker/Kubernetes) and cloud deployment for production-grade usage.  
- **Integration with deep learning frameworks**: Connect with PyTorch or TensorFlow for tasks involving symbolic + numeric hybrid models.  




