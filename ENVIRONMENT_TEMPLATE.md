# FastAPI Environment Configuration Template

Create your private environment variables in the FastAPI host’s secret manager. Do not commit a `.env` file, database password, or real JWT signing value to GitHub.

| Variable | Example format | Purpose |
|---|---|---|
| `DATABASE_URL` | `postgresql+psycopg://user:password@host:5432/careerlens` | PostgreSQL connection used by the authentication service. |
| `JWT_SECRET` | A long, unique random value | Signs access and refresh JWTs. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `15` | Short lifetime for bearer access tokens. |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `14` | Lifetime for rotated refresh tokens. |
| `CORS_ORIGINS` | `https://your-frontend.example.com` | Comma-separated approved browser origins. |
| `ENVIRONMENT` | `production` | Enables production-safe runtime behavior. |

After deploying the FastAPI service, set the public `VITE_AUTH_API_BASE_URL` value through the CareerLens project secret settings. The frontend uses this public HTTPS base URL to call the authentication API. No backend secret belongs in the frontend configuration.
