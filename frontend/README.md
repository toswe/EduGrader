# Frontend

React + TypeScript + Vite single‑page app for students and professors.

## Stack

- React 19 + React Router
- Vite
- Axios for API calls
- Served by Nginx in Docker

## Scripts

```bash
npm install
npm run dev      # start Vite dev server
npm run build    # type‑check and build to dist/
npm run preview  # preview built app locally
npm run lint
```

## Dev and API

- API base path: `/api`
- Dev server proxies `/api` per `vite.config.ts`
- In Docker, Nginx proxies `/api` to the backend (`nginx.conf`)

## Auth

- Access and refresh tokens are stored in `sessionStorage` as `accessToken` and `refreshToken`
- Axios interceptor adds `Authorization: Bearer <token>` and removes tokens on 401

## Run with Docker

From repository root:

```bash
docker-compose up -d
```

- App: http://localhost

## Structure

- `src/api/`: Axios instance and API modules
- `src/auth/`: Token utilities and auth wrapper
- `src/pages/`: Routes for student/professor
- `src/routes/`: Route guards and layouts
