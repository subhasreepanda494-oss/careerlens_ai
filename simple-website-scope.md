# CareerLens AI — Simplified Website Scope

## Current Deliverable

The current CareerLens AI deliverable is a **simple public website**. It introduces the product’s evidence-led career-preparation approach through a responsive landing page, explanatory feature sections, a short process, and clear navigation. Visitors do not need an account, a resume upload, an external API, or any private-workspace access.

## Deferred Work

The previously prepared FastAPI/PostgreSQL authentication implementation is intentionally **deferred and inactive** in the public website. The active page does not render sign-in, sign-up, protected routes, token storage, or calls to an external authentication service.

The backend material remains in the repository only as deferred technical work. It should be revived only if the product scope later changes from a simple information website to an authenticated application. If that happens, the external FastAPI service must be deployed, its PostgreSQL environment configured, and `VITE_AUTH_API_BASE_URL` set before any live account flow is enabled.

## Validation

The active website was checked with TypeScript, automated tests, and a production build. It was also reviewed at desktop and mobile viewports. The active public page contains no sign-in dependency and no simulated private access.
