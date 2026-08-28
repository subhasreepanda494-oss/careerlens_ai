# CareerLens AI — Phase 3 Authentication Checklist

- [x] Inspect the existing static project and determine the safest compatible approach for server-side authentication, persistence, and JWT refresh-token revocation.
- [x] Review the full-stack project guidance and authentication conventions before changing the project capability.
- [x] Confirm whether the project should use its newly available managed OAuth/session authentication or an externally hosted FastAPI/PostgreSQL password-and-JWT backend.
- [x] Read the persistent-service deployment guidance and define the FastAPI/PostgreSQL environment boundary for the selected external backend.
- [x] Add the required backend foundation, environment configuration, database migration, and FastAPI-compatible auth design without exposing secrets.
- [x] Implement and test signup, login, refresh, logout, current-user, validation, password hashing, CORS, and protected-endpoint behavior.
- [x] Add frontend auth state, typed API client token handling, refresh flow, protected routes, signup/login forms, validation, loading, and logout.
- [x] Verify desktop and mobile auth flows, run test/build checks, and prepare the requested Phase 3 documentation before pausing for Phase 4 approval.
- [x] Deploy the external FastAPI/PostgreSQL service, configure `VITE_AUTH_API_BASE_URL`, and run the live manual authentication checklist before starting Phase 4. (Deferred at the user’s request because the current deliverable is a simple public website.)
- [x] Await the deployed FastAPI service’s public HTTPS base URL from the user before configuring the frontend connection and executing live authentication checks. (Deferred at the user’s request because authentication is out of current scope.)
- [x] Replace the authentication-enabled application shell with a simple public CareerLens website that needs no sign-in or external backend.
- [x] Simplify calls to action, navigation, and content into clear public-site interactions without simulated private-workspace access.
- [x] Verify the simplified website on desktop and mobile, then document the deferred authentication work as out of current scope.
- [x] Re-run a final validation after documenting the simplified public-site scope and deferred authentication boundary.
- [x] Define shared CareerLens application state and evidence-label conventions for all user-provided, resume-extracted, source-based, and AI-generated content.
- [x] Build a responsive onboarding and resume upload flow with client-side PDF/DOCX validation, visible progress, and clear demo limitations.
- [x] Build the resume-analysis dashboard with extracted skills, strengths, role readiness, and an explainable resume signal.
- [x] Build job recommendations and a selected-job comparison that shows matched skills, missing skills, and a transparent match rationale.
- [x] Build a skill-gap roadmap with prioritized skills, learning actions, and progress interactions.
- [x] Build job-specific interview preparation and mock-answer feedback with clear AI-generated labels.
- [x] Build an application tracker and a single progress dashboard with user-controlled job status and next actions.
- [x] Verify desktop and mobile user journeys, run TypeScript/tests/build checks, and document which experiences remain simulated until connected to a backend.

- [x] Restore the previous recommended-job filter and sorting feature after the checkpoint rollback.
- [x] Add multi-select required-skill filtering and persist the selected filters for future browser visits.
- [x] Add application deadline data, deadline filtering, and closing-soon visual reminders to recommendation cards.
- [x] Extract recognizable skills locally from uploaded resume text and use them to auto-fill the required-skill filters.
- [x] Add unit tests, responsive screenshots, final build validation, and a corrected checkpoint for this feature update.

- [x] Inspect the CareerLens theme state, local persistence, CSS tokens, and hard-coded light-surface classes causing the toggle to appear ineffective.
- [x] Make dark/light theme selection persistent and apply readable dark-theme colors to the landing page, workspace shell, cards, filters, forms, and alerts.
- [x] Add theme behavior coverage and verify light and dark views at desktop and mobile sizes.

- [x] Add an automated test that mounts ThemeProvider, triggers the theme toggle, and verifies the root dark class and localStorage persistence.
- [x] Re-verify the interactive theme toggle itself in the browser, not only the query-parameter previews.

- [x] Reproduce the browser resume-reading failure for supported PDF/DOCX uploads and inspect extraction errors and status transitions.
- [x] Repair local PDF/DOCX extraction, display an accurate success/error/empty-text state, and auto-fill only skills actually detected from resume text.
- [x] Add extraction-flow coverage and verify the upload experience directly in the browser before saving the fix.

- [x] Add automated tests for PDF success, DOCX success, unreadable-file failure, and empty-text/no-selectable-text handling.
- [x] Add an explicit empty-text result and UI message distinct from generic browser read failure.
- [x] Verify a real DOCX upload in the browser and confirm detected skills auto-fill the job filters.
- [x] Save a new checkpoint after the fully validated resume-reading fix.

- [x] Add automated tests that call extractResumeText with valid PDF and valid DOCX fixtures, plus unreadable-file and empty-text cases.
- [x] After uploading a real DOCX in the browser, navigate to the jobs workspace and verify detected skills are preselected in required-skills filters.
- [x] Save a new checkpoint after the resume-reading fix is fully validated.

- [x] Verify the empty-text path through the extraction flow itself, not only the pure outcome helper.
- [x] After the DOCX upload, directly confirm the expected required-skill chips render in their selected active state.
- [x] Save a fresh checkpoint after the resume-reading fix passes all validation.

- [x] Create a private GitHub repository for the current CareerLens source and push the latest validated project state. (Superseded: the connected GitHub integration lacked create/push permission, so a complete verified source archive is supplied for manual upload.)
- [x] Verify the remote default branch and deliver the repository URL. (Superseded by the manual-upload archive delivery.)
- [x] Confirm that publishing the CareerLens source to the specified public GitHub repository is intentional before pushing. (Confirmed by the user.)

- [x] Prepare a complete CareerLens source archive excluding dependencies, build outputs, local environment files, and repository metadata.
- [x] Verify the archive contains the frontend, backend-ready source, tests, documentation, configuration, and package manifest files needed for manual GitHub upload.
- [x] Confirm the archive includes representative frontend, backend, test, documentation, package, and configuration files before delivery.
- [x] Document the non-secret backend configuration contract in a safe Markdown source file and include it in the verified GitHub upload archive. (An `.env.example` file is intentionally not created.)
- [x] Rebuild the verified archive with the finalized checklist and deliver it for manual GitHub upload.
