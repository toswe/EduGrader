# Master

Full‑stack platform for course and test management with automated grading.

## Project structure

- `backend/`: Django REST API for authentication, courses/tests, and grading
- `frontend/`: React + TypeScript + Vite single‑page application (student & professor flows)

## Quick start (Docker)

From the repository root:

```bash
docker-compose up -d
```

- API: http://localhost:8000
- Web app: http://localhost

## Backend

Powered by Django, DRF, JWT auth, and grading integrations (OpenAI, Gemini). See detailed setup, commands, and environment in:

- `backend/README.md`

## Frontend

Vite + React + TypeScript SPA served by Nginx in Docker. For local dev and scripts, see:

- `frontend/README.md`

