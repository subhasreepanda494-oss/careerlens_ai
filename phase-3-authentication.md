# CareerLens AI — Phase 3 Authentication Delivery

## Completed Scope

Phase 3 implements the selected **FastAPI + PostgreSQL + email/password JWT** architecture without replacing the Phase 2 CareerLens UI. The FastAPI service is contained in `backend/` for external deployment. The frontend uses an explicit API boundary and will protect every `/app/*` route; it does not create a local or demo authentication session when the external service is unavailable.

## Files Created or Modified

| Area | Files | Change |
|---|---|---|
| FastAPI core | `backend/app/core/config.py`, `backend/app/core/security.py`, `backend/app/database.py`, `backend/app/main.py` | Environment-driven config, Argon2 hashing, JWT signing/validation, SQLAlchemy engine, CORS, health route |
| Data model | `backend/app/models.py`, `backend/alembic/versions/20260826_0001_create_auth_tables.py` | PostgreSQL users and refresh-token persistence/revocation model |
| Auth API | `backend/app/api/deps.py`, `backend/app/api/routes/auth.py`, `backend/app/services/auth.py`, `backend/app/schemas/auth.py` | Signup, login, refresh, logout, current-user and safe forgot-password flow |
| Backend tooling | `backend/requirements.txt`, `backend/alembic.ini`, `backend/alembic/env.py`, `backend/pytest.ini`, `backend/README.md` | Runtime, migration, test and Replit deployment instructions |
| Frontend auth | `client/src/features/auth/AuthProvider.tsx`, `CareerAuthScreen.tsx`, `SessionSignOut.tsx` | API client, token refresh, session persistence, forms, errors, loading, protected-route and logout state |
| Existing UI | `client/src/App.tsx`, `client/src/pages/Home.tsx` | Auth provider integration, protected workspace route, real identity display in top bar/profile |
| Tests | `backend/tests/test_auth.py`, `client/src/features/auth/AuthProvider.test.tsx`, `vitest.config.ts` | Backend and frontend validation coverage |

## Database Migration

The new Alembic revision creates `users` and `refresh_tokens`. `refresh_tokens` stores a one-way token digest, JWT identifier, expiry, revocation time, and replacement linkage. It supports refresh-token rotation and logout revocation without saving raw refresh tokens. Run `alembic upgrade head` against the external PostgreSQL database before launching the FastAPI service.

## Required Deployment Configuration

The external FastAPI host must define `DATABASE_URL`, `JWT_SECRET`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`, `CORS_ORIGINS`, and `ENVIRONMENT`. After the FastAPI service has a public HTTPS URL, configure `VITE_AUTH_API_BASE_URL` in the CareerLens project secret manager. No database URL, JWT secret, or password has been placed in client code or committed to this project.

## Installation, Run, and Test Commands

```bash
# FastAPI service
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port $PORT

# Backend tests
cd backend
pytest -q

# CareerLens frontend tests and build
cd ..
pnpm check
pnpm test
pnpm build
```

## Manual Testing Checklist

| Scenario | Expected result |
|---|---|
| Open `/app/dashboard` while unauthenticated | Redirect to `/login` |
| Register with a valid password | API creates user and returns a token pair; UI routes to dashboard |
| Register duplicate email | API returns a friendly duplicate-account error |
| Sign in with incorrect credentials | API returns a generic invalid-credentials error |
| Refresh a valid session | Access and refresh token rotate; current user reloads |
| Reuse old refresh token | API rejects it after rotation |
| Sign out | Refresh token is revoked and browser session is cleared |
| Forgot password | UI shows the safe development-not-configured response |
| Omit `VITE_AUTH_API_BASE_URL` | UI stays at secure sign-in and reports that authentication is not configured; it does not create a demo session |

## Validation Performed

The FastAPI test suite passed **7 tests**. The CareerLens frontend passed TypeScript checking, **3 Vitest tests**, and a production build. The Alembic migration successfully applied to an isolated local database. The login screen and protected-route redirect were visually verified while the external API URL remained unconfigured.

## Security Notes

The service uses Argon2 password hashing, short-lived HMAC-SHA256 JWT access tokens, refresh-token rotation, persistent revocation data, bearer-token protection for `/me`, typed validation, and restrictive explicit CORS origins. Password reset is intentionally a no-email placeholder until an email provider is separately configured. Because the backend is not yet deployed, live browser authentication cannot be tested until the external PostgreSQL service and its HTTPS URL are available.

## What Remains Before Phase 4

External deployment and configuration must be completed first: provision PostgreSQL, set the FastAPI environment variables, run the Alembic migration, deploy the service, configure `VITE_AUTH_API_BASE_URL`, then complete the live manual authentication checklist. Phase 4 work must not begin until the user explicitly requests it.
