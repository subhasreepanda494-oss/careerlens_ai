# CareerLens AI FastAPI Authentication Service

This folder is the **external FastAPI/PostgreSQL authentication service** selected for CareerLens AI. It is intentionally independent from the managed React project: it owns password hashing, JWT issuance, refresh-token rotation and revocation, and user identity. The React client is already prepared to call it once its public HTTPS URL is configured.

## Service Contract

| Endpoint | Method | Purpose |
|---|---:|---|
| `/health` | `GET` | Deployment health check |
| `/api/v1/auth/signup` | `POST` | Register an account and return access/refresh tokens |
| `/api/v1/auth/login` | `POST` | Authenticate credentials and return access/refresh tokens |
| `/api/v1/auth/refresh` | `POST` | Rotate a valid refresh token and issue a new access token |
| `/api/v1/auth/logout` | `POST` | Revoke the submitted refresh token |
| `/api/v1/auth/me` | `GET` | Return the bearer-token holder’s profile |
| `/api/v1/auth/forgot-password` | `POST` | Return the development-safe notice that email delivery is not configured |

## Required Runtime Configuration

Set the following values in the FastAPI host’s secret/environment manager. Do **not** commit them to source control. `JWT_SECRET` must be a unique, long random value. `CORS_ORIGINS` must name the actual frontend origin, without a wildcard.

| Variable | Example shape | Purpose |
|---|---|---|
| `DATABASE_URL` | `postgresql+psycopg://user:password@host:5432/careerlens` | PostgreSQL connection string |
| `JWT_SECRET` | Long random secret | HMAC key for access and refresh JWTs |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `15` | Short access-token lifetime |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `14` | Refresh-token lifetime |
| `CORS_ORIGINS` | `https://frontend.example.com` | Comma-separated browser origins allowed to call the service |
| `ENVIRONMENT` | `production` | Disables public API documentation in production |

After deployment, set the **public** `VITE_AUTH_API_BASE_URL` value in the CareerLens web project’s secret manager to the service URL, without a trailing slash. This is the only frontend configuration value; it is not a credential.

## Replit-Ready Commands

From this `backend/` directory, create the Replit Python environment, then install and run the service with the following commands.

```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

For local development only, set `PORT=8000` before the final command. Configure the production frontend origin in `CORS_ORIGINS` before testing browser requests.

## Tests

Run the backend suite from this directory.

```bash
pytest -q
```

The suite covers successful sign-up, duplicate accounts, invalid email and password input, successful and failed sign-in, invalid/expired protected access, refresh-token rotation, refresh-token reuse rejection, and logout revocation. The tests use an isolated SQLite database only for local execution; production requires PostgreSQL.

## Security Model

Passwords are hashed by Argon2 and are not logged, returned, or stored in raw form. Access tokens are short-lived JWTs sent by the client in the `Authorization: Bearer` header. Refresh tokens are held in the client’s selected browser storage according to “Remember me,” but the database holds only a SHA-256 digest and token identifier—not the raw value. Each refresh revokes the previous token before issuing a replacement; logout revokes the supplied active refresh token. Authentication failures use concise, non-enumerating messages.

> The current browser flow deliberately stays unavailable until `VITE_AUTH_API_BASE_URL` is configured. It does not fall back to a fabricated session.
