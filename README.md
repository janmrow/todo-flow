# One-Line To-Do (Flask + SQLite)

Small, test-friendly To-Do app built as a playground for QA + DevOps.

---

## 🚀 Run locally

1. **Setup Environment**
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt

2. **Initialize Database**
export FLASK_APP=app
flask init-db

3. **Run Application**
flask run
Open: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🛠 Testing & Docker

* Run tests: pytest -q
* Run with Docker: docker compose up --build
* Health check: GET /api/health
* Run E2E tests (Playwright) with Docker: docker compose run --rm e2e
---
