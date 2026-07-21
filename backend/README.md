# Backend

Minimal Django REST API powering authentication, course/test management, and automated grading.

## Stack

- Django 5 + Django REST Framework
- JWT auth via `djangorestframework-simplejwt`
- CORS via `django-cors-headers`
- Default DB: SQLite (dev)

## Apps

- `authentification`: Custom `User` model and auth endpoints
- `backend`: Core models for courses, tests, student attempts
- `grading`: Grading pipeline with LLM integrations (OpenAI, Gemini)

## Run (Docker)

From repository root:

```bash
docker-compose up -d backend
```

The API will be available at `http://localhost:8000/`.

## Run (Local)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Environment

- Docker uses `.env.dev` at the repo root. For local runs, export equivalent variables or create a `.env` and load as needed.


