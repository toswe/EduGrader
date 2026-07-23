# Master

Full‑stack platform for course and test management with automated grading.

## Project structure

- `backend/`: Django REST API for authentication, courses/tests, and grading
- `frontend/`: React + TypeScript + Vite single‑page application (student & professor flows)
- `thesis/`: Master's thesis (LaTeX), compiled automatically via GitHub Actions

## Thesis

[![Compile thesis](https://github.com/toswe/Master/actions/workflows/thesis.yml/badge.svg)](https://github.com/toswe/Master/actions/workflows/thesis.yml)

**[View the latest PDF](https://toswe.github.io/Master/main.pdf)** (compiled automatically on every push to `main`).

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

