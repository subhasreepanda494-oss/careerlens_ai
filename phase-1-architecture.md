# CareerLens AI — Phase 1 Product Architecture

## 1. Product Scope and Architectural Position

CareerLens AI is a **career-intelligence SaaS platform** that converts candidate-provided resume evidence into transparent, action-oriented analysis: a structured candidate profile, role matching, skill-gap prioritisation, interview preparation, and a career roadmap. The platform must clearly separate three information classes: **resume-extracted facts**, **source-backed external job data**, and **AI-generated recommendations**. That provenance requirement is a product rule expressed in the data model, API responses, and interface—not merely in copy.

The implementation is intentionally phased. Phase 1 establishes the target architecture and interface specification; it does **not** claim that authentication, file parsing, live job data, or LLM analysis is already operational. The current static project will serve as the frontend foundation. A future service upgrade or connected backend environment is required before implementing secure authentication, PostgreSQL persistence, document processing, or private API integration.

| Layer | Recommended technology | Responsibility | Phase-1 status |
|---|---|---|---|
| Web client | React, Vite, TypeScript, Tailwind, Recharts, Lucide | User experience, visualisation, client-side validation, routing | Foundation selected |
| Application API | Python, FastAPI, Pydantic, SQLAlchemy/Alembic | Authentication, validation, orchestration, REST endpoints | Specified, not yet implemented |
| Persistence | PostgreSQL | Durable user, resume, analysis, job, interview, and progress data | Specified, not yet provisioned |
| Document intelligence | PyMuPDF/pdfplumber, python-docx, optional OCR | Extract text and resume fields from uploaded documents | Specified, not yet implemented |
| AI orchestration | Server-side LLM client using environment variables | Generate summaries, recommendations, questions, and feedback | Specified, not yet connected |
| Matching / ML | Deterministic skills taxonomy plus scikit-learn where justified | Explainable role compatibility and priority scoring | Specified, not yet implemented |
| External jobs | Reliable permitted job API or search connector | Fetch and retain source attribution for live vacancy information | Conditional; never simulated as current data |

## 2. System Architecture Diagram

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                           CareerLens AI React Client                         │
│ Landing · Auth · Dashboard · Resume · Jobs · Interview · Roadmap · Settings │
└───────────────┬──────────────────────────────────────────────────────────────┘
                │ HTTPS / typed REST client / bearer token
                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                              FastAPI Application                             │
│  Auth Router · Resume Router · Jobs Router · Interview Router · Plan Router │
│  Validation · Authorization · Rate limits · Audit/provenance enforcement    │
└───────┬────────────────────┬─────────────────────┬───────────────────────────┘
        │                    │                     │
        ▼                    ▼                     ▼
┌───────────────┐  ┌────────────────────┐  ┌─────────────────────────────────┐
│ PostgreSQL    │  │ Resume Pipeline    │  │ AI & Matching Orchestration     │
│ Users         │  │ Secure storage     │  │ Skills taxonomy                 │
│ Resumes       │  │ PDF/DOCX parser    │  │ Match scoring                   │
│ Skills        │  │ Structured fields  │  │ LLM API via server-side secret  │
│ Jobs/matches  │  │ Evidence map       │  │ Provenance-labelled outputs     │
│ Interviews    │  └────────────────────┘  └─────────────────────────────────┘
│ Plans/history │
└───────┬───────┘
        │
        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ Trusted External Sources (optional and consent-aligned)                      │
│ Job API/search source → source URL, retrieval timestamp, available fields   │
│ No fabricated listing, salary, deadline, or interview-date records           │
└──────────────────────────────────────────────────────────────────────────────┘
```

## 3. Frontend Architecture

The frontend is a modular React client organised around domain slices, shared UI primitives, and typed service boundaries. It should use React Query or an equivalent query layer in the backend-connected phase for cache, retries, loading states, and error recovery. Wouter can remain the lightweight route layer. A central `apiClient` maps typed request and response DTOs rather than allowing page components to call endpoints directly.

| Area | Components / modules | Key responsibilities |
|---|---|---|
| Public experience | `LandingPage`, `FeatureSection`, `Footer` | Explain product, surface provenance principles, route visitors to onboarding |
| Identity | `LoginPage`, `SignupPage`, `ForgotPasswordPage`, `AuthGuard` | Secure sign-in flow, protected-route redirects, session lifecycle |
| Workspace shell | `AppShell`, `Sidebar`, `Topbar`, `ThemeToggle` | Responsive navigation, light/dark mode, profile menu, mobile drawer |
| Resume domain | `ResumeUpload`, `UploadState`, `ResumeProfile`, `ResumeScore` | PDF/DOCX client validation, upload progress, evidence-labelled analysis |
| Jobs domain | `JobSearch`, `JobFilters`, `JobCard`, `JobDetails` | Search, source-aware listings, match explanation, external apply URLs |
| Interview domain | `Countdown`, `QuestionSet`, `MockInterviewSession`, `AnswerReview` | Interview date entry, dynamic questions, timed one-question flow, feedback |
| Planning domain | `SkillGapPanel`, `PreparationPlan`, `CareerRoadmap` | Prioritised gaps, daily plans, role-path comparisons, progress tracking |
| Shared states | `LoadingSkeleton`, `EmptyState`, `ErrorState`, `ProvenanceBadge` | Consistent loading, recoverable errors, no-data guidance, data labels |

### Frontend Route Map

| Route | Screen | Access | Primary action |
|---|---|---|---|
| `/` | Landing | Public | Start resume analysis |
| `/login` | Login | Public | Authenticate user |
| `/signup` | Signup | Public | Create account |
| `/forgot-password` | Password recovery | Public | Request reset instructions |
| `/app/dashboard` | Dashboard | Protected | Review most valuable next action |
| `/app/resume` | Resume Analyzer | Protected | Upload or review parsed resume |
| `/app/jobs` | Job Recommendations | Protected | Filter and compare source-backed jobs |
| `/app/jobs/:jobId` | Job Details | Protected | Review match evidence and action plan |
| `/app/interview` | Interview Preparation | Protected | Set date and generate preparation content |
| `/app/mock-interview` | Mock Interview | Protected | Start or resume question session |
| `/app/skill-gaps` | Skill Gap Analysis | Protected | Prioritise learning gaps |
| `/app/preparation-plan` | Preparation Roadmap | Protected | Complete daily preparation tasks |
| `/app/career-roadmap` | Career Roadmap | Protected | Compare suitable career paths |
| `/app/profile` | Profile | Protected | Maintain preferences and personal information |
| `/app/settings` | Settings | Protected | Manage theme, privacy, data and account controls |

## 4. Backend Architecture

The FastAPI service should be structured by business capability. Routers remain thin: they authenticate, validate Pydantic payloads, and call explicit services. Services orchestrate persistence, document extraction, matching, and AI generation. Repositories own database queries. Provider adapters isolate vendor-specific LLM and job-source implementation details, so a change in external service does not change the rest of the application.

| Backend layer | Contents | Design rule |
|---|---|---|
| `api/routers` | Versioned REST endpoints | No persistence or LLM implementation in routers |
| `schemas` | Pydantic inputs and responses | Explicit response fields and provenance metadata |
| `services` | Auth, resume, matching, interview, planning workflows | Business rules and transactional boundaries live here |
| `repositories` | SQLAlchemy queries | No presentation logic; enforce tenant/user ownership |
| `models` | SQLAlchemy ORM models | Relationships, indexes, timestamps, status fields |
| `parsers` | PDF/DOCX text + field extraction | Never infer missing resume facts; preserve evidence fragments |
| `ai` | Provider adapter, prompt templates, output validation | Server-only secret usage, safe structured output, recommendation labels |
| `integrations` | Job providers/search connectors | Preserve source, retrieved timestamp, missing values as unavailable |
| `core` | Config, security, logging, exceptions | Environment-driven configuration; no secrets in source code |

## 5. Database Architecture

PostgreSQL is the system of record. All user-visible analyses are versioned against the resume and job context that created them. Rows include created/updated timestamps, ownership references, and status to make asynchronous processing observable.

```text
User 1 ─── * Resume 1 ─── * ResumeExtraction 1 ─── * ResumeSkill
  │              │
  │              └──── * ResumeAnalysis
  │
  ├──── * JobMatch * ─── 1 Job
  ├──── * Interview 1 ─── * InterviewQuestion
  ├──── * MockInterview 1 ─── * MockInterviewTurn
  ├──── * PreparationPlan 1 ─── * PreparationTask
  └──── * CareerRoadmap 1 ─── * CareerPathRecommendation
```

| Table | Key fields | Purpose |
|---|---|---|
| `users` | `id`, `email`, `password_hash`, `display_name`, `preferences_json` | Identity and user preferences |
| `resumes` | `id`, `user_id`, `file_name`, `mime_type`, `storage_key`, `parse_status` | Resume asset metadata and processing state |
| `resume_extractions` | `resume_id`, `normalized_json`, `evidence_json`, `extractor_version` | Structured facts and source text locations |
| `skills` | `id`, `canonical_name`, `category` | Controlled skills taxonomy |
| `resume_skills` | `resume_id`, `skill_id`, `evidence`, `confidence` | Skills linked only when supported by resume evidence |
| `resume_analyses` | `resume_id`, `score_json`, `summary`, `recommendations_json`, `model_metadata` | Versioned score and AI recommendations |
| `jobs` | `id`, `provider`, `source_url`, `external_id`, `retrieved_at`, `raw_json` | Source-backed vacancy fields and provenance |
| `job_matches` | `user_id`, `resume_id`, `job_id`, `match_score`, `matched_skills_json`, `missing_skills_json` | Explainable candidate-to-job comparison |
| `interviews` | `user_id`, `job_id`, `scheduled_at`, `mode`, `location`, `source_type` | User-entered or source-backed interview details; never guessed |
| `interview_questions` | `interview_id`, `category`, `prompt`, `priority`, `generation_context` | Clearly labelled AI-generated preparation questions |
| `mock_interviews` | `user_id`, `job_id`, `type`, `difficulty`, `status`, `final_score` | Mock-session metadata and outcome |
| `mock_interview_turns` | `mock_interview_id`, `question`, `answer`, `feedback_json`, `sequence` | One-question-at-a-time interview evidence and feedback |
| `preparation_plans` | `user_id`, `job_id`, `start_date`, `end_date`, `status` | Personalised preparation-plan container |
| `preparation_tasks` | `plan_id`, `day_index`, `title`, `rationale`, `completed_at` | Dynamic daily tasks and completion state |
| `career_roadmaps` | `user_id`, `resume_id`, `recommendations_json` | Candidate-specific role-path analysis |

## 6. AI and Matching Architecture

The intelligence layer must follow an **evidence-first, recommendation-second** pipeline.

1. A document parser produces text plus source fragments.
2. A deterministic extractor/taxonomy maps explicitly supported information into the candidate profile. The system stores the evidence fragment for every extracted skill where possible.
3. The matching service compares canonical candidate skills, experience, education, and stated user preferences against structured job requirements. Deterministic weighting provides an explainable base match.
4. An LLM can summarise the candidate profile, prioritise missing skills, draft practice questions, create preparation tasks, and evaluate mock answers. The prompt receives only validated structured context; it must return an explicitly typed response.
5. Output validation rejects unsupported factual claims. All LLM-created material is stored with model/version metadata and displayed as **AI-generated recommendations**.

| Output | Evidence class | Required user-facing label |
|---|---|---|
| Name, skill, degree, project parsed from document | Extracted / verified resume information | “Extracted from your resume” |
| Job title, company, source URL, posted date from provider | Source-backed external information | “Source: [provider]” |
| Salary calculated from a stated public source | Source-backed or estimated | “Source-backed salary” or “Estimated salary range” |
| Interview date entered by the user | User-provided information | “Added by you” |
| Summary, improvement, career path, question, task, feedback | AI-generated recommendation | “AI-generated recommendation” |
| Missing vendor-provided fields | Not available | “Not available” / “Interview date has not been announced” |

## 7. REST API Surface (v1)

All protected endpoints require an authenticated user identity, apply ownership checks, and return structured errors. AI-generation endpoints should rate-limit per user and persist a traceable generation record.

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/api/v1/auth/register` | Create account with securely hashed password |
| `POST` | `/api/v1/auth/login` | Authenticate and issue secure session/token |
| `POST` | `/api/v1/auth/logout` | Revoke active session/token |
| `POST` | `/api/v1/auth/forgot-password` | Begin password reset workflow |
| `GET` | `/api/v1/me` | Return current profile and preferences |
| `PATCH` | `/api/v1/me` | Update allowed profile fields/preferences |
| `POST` | `/api/v1/resumes` | Initiate validated PDF/DOCX upload |
| `GET` | `/api/v1/resumes/{resume_id}` | Get metadata and parse/analysis status |
| `POST` | `/api/v1/resumes/{resume_id}/parse` | Parse and normalise document content |
| `POST` | `/api/v1/resumes/{resume_id}/analyze` | Run scoring and labelled AI analysis |
| `GET` | `/api/v1/resumes/{resume_id}/analysis` | Get score, evidence, strengths and improvements |
| `GET` | `/api/v1/jobs` | Query permitted source-backed jobs and filters |
| `GET` | `/api/v1/jobs/{job_id}` | Get a job with source attribution and availability fields |
| `POST` | `/api/v1/jobs/{job_id}/match` | Create/retrieve explainable resume-to-job match |
| `GET` | `/api/v1/jobs/{job_id}/match` | Retrieve matched/missing skills and recommendations |
| `GET` | `/api/v1/interviews` | List user interviews |
| `POST` | `/api/v1/interviews` | Create user-provided interview date/details |
| `PATCH` | `/api/v1/interviews/{interview_id}` | Correct user-entered interview details |
| `POST` | `/api/v1/interviews/{interview_id}/questions` | Generate labelled preparation questions |
| `GET` | `/api/v1/interviews/{interview_id}/questions` | Fetch generated questions and priorities |
| `POST` | `/api/v1/mock-interviews` | Start a mock interview configuration |
| `POST` | `/api/v1/mock-interviews/{id}/turns` | Submit answer; receive contextual feedback and next question |
| `POST` | `/api/v1/mock-interviews/{id}/complete` | Produce final readiness score and improvement plan |
| `GET` | `/api/v1/skill-gaps` | Return role-specific current/required/missing skill analysis |
| `POST` | `/api/v1/preparation-plans/generate` | Generate dynamic plan from date, role, gaps, and level |
| `GET` | `/api/v1/preparation-plans/current` | Read current plan and task state |
| `PATCH` | `/api/v1/preparation-tasks/{task_id}` | Mark plan task complete/incomplete |
| `GET` | `/api/v1/career-roadmap` | Return relevant path recommendations and gap steps |

## 8. Recommended Repository Structure

```text
careerlens-ai/
├── frontend/                                # React client (current static project foundation)
│   ├── src/
│   │   ├── app/                             # Router, providers, application shell
│   │   ├── components/                      # Shared UI components
│   │   │   ├── brand/                       # Logo, wordmark, provenance badge
│   │   │   ├── charts/                      # Recharts wrappers and insight annotations
│   │   │   ├── layout/                      # Shell, navigation rail, mobile menu
│   │   │   └── states/                      # Skeleton, empty, error, loading states
│   │   ├── features/                        # Domain modules, independently testable
│   │   │   ├── auth/
│   │   │   ├── dashboard/
│   │   │   ├── resumes/
│   │   │   ├── jobs/
│   │   │   ├── interviews/
│   │   │   ├── mock-interviews/
│   │   │   ├── preparation/
│   │   │   └── career-roadmap/
│   │   ├── pages/                           # Route-level page composition
│   │   ├── services/                        # Typed HTTP client and endpoint modules
│   │   ├── hooks/                           # Shared client hooks
│   │   ├── types/                           # DTOs, domain models, API error types
│   │   ├── lib/                             # Formatting, scoring and UI utilities
│   │   └── styles/                          # Tokens, global styles, animation rules
│   ├── tests/                               # Component and client-flow tests
│   ├── .env.example                         # Public build variables only, never secrets
│   ├── netlify.toml                         # SPA redirects and build settings
│   └── package.json
├── backend/                                 # FastAPI service (future implementation phase)
│   ├── app/
│   │   ├── api/v1/routers/
│   │   ├── ai/
│   │   ├── core/
│   │   ├── database/
│   │   ├── integrations/
│   │   ├── models/
│   │   ├── parsers/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── alembic/
│   ├── tests/
│   ├── .env.example
│   └── requirements.txt
├── docs/
│   ├── architecture.md
│   ├── figma-spec.md
│   ├── integration-guides.md
│   └── testing-strategy.md
├── infra/
│   ├── docker-compose.yml                   # Local development only
│   └── ci/
├── README.md
└── .gitignore
```

## 9. Development Roadmap

| Phase | Deliverable | Acceptance focus |
|---|---|---|
| 1 | Product architecture, data/provenance rules, design specification | All claims have a designated source class and implementation boundary |
| 2 | UI/UX system and visual prototype | Responsive, accessible, branded screens with clear states |
| 3 | Frontend foundation | App shell, routing, typed domain models, component library, demo-safe states |
| 4 | Authentication | Secure server-side hashing, session policy, protected routes |
| 5 | Resume upload and parser | PDF/DOCX validation, status states, source evidence, privacy handling |
| 6 | Resume intelligence | Versioned score, evidence-based analysis, labelled recommendations |
| 7 | Job integrations and recommendation engine | Permitted source-backed listing ingestion and explainable matches |
| 8 | Job details and skill matching | Clear matched/missing skills, availability fallbacks, source attribution |
| 9 | Interview information and countdown | User-entered dates, live countdown, no invented scheduling data |
| 10 | Interview question generation | Context-bound, priority-labelled practice question sets |
| 11 | Mock interview | Turn-based session, structured feedback, readiness score provenance |
| 12 | Preparation plan | Dynamic daily plan, task progress, remaining-day logic |
| 13 | Career roadmap | Candidate-relevant role options, gaps, suggested projects, steps |
| 14 | Database integration and migrations | Data ownership, durable state, backups, migrations, observability |
| 15 | Quality assurance | Unit, integration, API, accessibility, security and error-path testing |
| 16 | Deployment readiness | Production config, SPA redirects, secret management, deployment smoke tests |

## 10. Figma Screen Plan

The design system is shared across every screen: Lens Blue primary actions; Indigo Ink editorial hierarchy; Aubergine Violet AI labels; DM Serif Display headings; Manrope UI/body text; 8px spacing rhythm; 14px standard card radius; navigation rail on desktop and a bottom-accessible drawer on mobile. Every screen supports light and dark themes and presents labels for extracted, source-backed, user-provided, and AI-generated information.

| Screen | Layout and key components | Main interaction and responsive behavior |
|---|---|---|
| Landing | Editorial split hero, workflow timeline, six feature cards, source-truth promise, footer | Hero CTAs route to signup/features; image field stacks below copy on mobile |
| Login | Focused two-column auth panel, credential form, password visibility, recovery link | Inline validation and loading button; art panel removed on compact screens |
| Signup | Account form, consent/terms acknowledgement, benefits sidebar | Password guidance and submit state; sidebar collapses under form on mobile |
| Dashboard | Navigation rail, career brief header, score lens, next action shelf, chart modules | Cards route to focused workspaces; rail becomes drawer at tablet/mobile |
| Resume Analyzer | Upload well, processing timeline, resume overview, evidence chips, score rings | Drop/upload control, retry action, evidence expansion; chart stack on mobile |
| Resume Results | Candidate profile, score breakdown, strengths and improvement annotations | Tabs/anchor rail; explicit verified vs AI-generated label toggles |
| Job Recommendations | Filter strip, jobs list, match comparison panel, source chips | Search/filter/reset, job-card click, external apply action only when source URL exists |
| Job Details | Role brief, job facts, fit evidence, gap priorities, interview-availability panel | Apply uses source URL; unavailable fields remain visibly unavailable |
| Interview Preparation | Countdown, question categories, preparation timeline, date entry modal | User-entered date updates plan; question expansion and priority filters |
| Mock Interview | Focus panel, question queue, answer editor/mic affordance, feedback rail | One-question flow, clear completion view; microphone only appears when supported |
| Skill Gap | Role selector, match ring, current/required/missing skill columns, priority ladder | Role comparison updates interpretation; columns stack in a clear order on mobile |
| Preparation Roadmap | Day-by-day task ledger, progress meter, rationale drawer | Mark tasks complete, filter remaining; horizontal timeline becomes vertical mobile list |
| Career Roadmap | Candidate profile header, career-path cards, missing-skill sequences, project prompts | Compare role paths, open action plan; card deck becomes swipe-friendly stack |
| Profile | Identity block, stated preferences, location/career objective controls | Save with explicit success/error state; no resume facts editable without source warning |
| Settings | Settings sections for appearance, notifications, privacy, account | Toggles, confirmation dialogs, data-export/destructive action protections |

## 11. Lovable Integration Plan

Lovable can be used to accelerate the visual frontend only after this specification is accepted. Provide it a prompt that instructs it to generate a React/TypeScript/Tailwind client organised by the `features/` structure above, using typed service stubs—**not fabricated network data**. It should render clearly marked demo data only in an explicit Demo Mode and must not show artificial current jobs, salaries, deadlines, employer facts, or testimonials.

The frontend interface contract will use the endpoint paths and DTO concepts defined in this document. A generated client must encapsulate endpoint calls in `services/`, with page components consuming hooks rather than direct `fetch` calls. All non-functional controls must either be wired to a local demonstrable interaction (theme switch, filter state, demo flow) or omitted until backend support is available.

## 12. Replit-Ready Backend Plan

The backend target is a Python 3.11+ FastAPI service deployable in a Replit or comparable web-service environment. Dependencies should include `fastapi`, `uvicorn`, `pydantic-settings`, `sqlalchemy`, `alembic`, `psycopg`, `passlib[bcrypt]` or `argon2-cffi`, `python-multipart`, a PDF parser, `python-docx`, `httpx`, and a selected server-side LLM SDK. `scikit-learn` should be introduced only after an explainable deterministic matching baseline has been validated.

The environment must contain `DATABASE_URL`, `AI_API_KEY`, `SECRET_KEY`, `CORS_ORIGINS`, and any job-provider credentials. No values appear in frontend builds or Git history. Launch with `uvicorn app.main:app --host 0.0.0.0 --port $PORT`; use `/docs` only in non-production/internal environments and a dedicated `/health` endpoint for deployment checks. Integrate database migrations with Alembic before implementing irreversible data changes. API tests should use ephemeral test databases and mocked LLM/job-provider adapters.

## 13. Netlify-Ready Frontend Plan

The React/Vite frontend can deploy to Netlify with build command `pnpm build` and publish directory `dist/public` if the existing build pipeline continues to emit the client bundle there; this must be verified in Phase 16. Add an SPA redirect such as `/* /index.html 200` in `netlify.toml` or a Netlify redirects file so protected client routes refresh correctly. The frontend receives only a public `VITE_API_BASE_URL` (and similarly public build-time configuration); it must never receive `AI_API_KEY`, `SECRET_KEY`, `DATABASE_URL`, or job-provider secrets.

Before release, validate the production API base URL, CORS allowlist, route-refresh behavior, authenticated redirect behavior, core error states, accessibility, source attribution, and the absence of private values in the built assets. Manus provides built-in hosting and domain management for this project; if an external Netlify deployment is later chosen, it should be validated independently for compatibility.

## Phase 1 Decision Log

1. CareerLens AI will prioritise **information provenance** over generic “AI” claims.
2. The client starts as a static visual foundation; secure data, parsing, AI, and integrations require a backend-enabled phase.
3. Resume facts are never invented; live job facts are never fabricated; generated advice is always labelled.
4. UI controls will only appear when implemented or meaningfully demonstrable in an explicitly labelled Demo Mode.
5. The next requested work should be **Phase 2: UI/UX design and frontend prototype**, pending user confirmation.

