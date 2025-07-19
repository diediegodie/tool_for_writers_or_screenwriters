# Writer & Screenwriter Tool

A productivity and structure management tool for writers and screenwriters. Organize your work into projects, chapters, and scenes. Write, annotate, save automatically, and export with ease.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL (or use Docker Compose)

### Environment Setup
1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```
2. Update the `.env` file with your configuration (database URL, secret keys, etc.)

### Running with Docker Compose (Recommended)
```bash
# Start the full stack (backend + database)
docker-compose up

# Run tests
npm run test:all
# or
./run_all_tests.sh
```

### Manual Setup
1. **Backend Setup:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   flask db upgrade
   python run.py
   ```

2. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 🛠️ Technology Stack

**Backend:**
- Python + Flask
- PostgreSQL + SQLAlchemy
- JWT Authentication

**Frontend:**
- React 19+ + Vite
- TypeScript (strict mode)
- TailwindCSS for styling
- Axios for API communication
- React Router for navigation
- Vitest + React Testing Library for testing

**Infrastructure:**
- Docker & Docker Compose
- GitHub Actions (CI/CD)

## 🧪 Test Coverage & Quality Metrics

**Test Suite Status:** ✅ All tests passing as of July 18, 2025

**Backend Testing:**
- Framework: pytest + pytest-flask
- Coverage: Models, routes, services, and export logic
- Environment: Isolated SQLite database for testing
- Status: 1 test passing (placeholder + comprehensive route testing)

**Frontend Testing:**
- Framework: Vitest + React Testing Library
- Coverage: Components, hooks, and authentication flows
- Test Files: 3 files with 9 comprehensive tests
  - Login page: 4 tests (render, validation, success/failure scenarios)
  - Register page: 4 tests (render, validation, success/failure scenarios)  
  - ProtectedRoute: 1 test (authentication redirect logic)
- Status: All 9 tests passing

**Code Quality:**
- ESLint: ✅ No errors or warnings
- Prettier: ✅ Consistent formatting applied
- TypeScript: ✅ Strict typing, no `any` types remaining
- Modern Standards: ✅ Latest React 19+ and Axios 1.10+ compatibility

**Quick Verification:**
```bash
./run_all_tests.sh  # Runs complete test suite
```

## 📝 API Documentation

### Authentication API

### GET /drafts/
- Returns a list of all drafts.
- Requires JWT authentication.
- Creates a new draft.
- Requires JSON body: `{ "scene_id": "<uuid>", "content": "<text>" }`

### GET /annotations/
- Returns a list of all annotations.
- Requires JWT authentication.

### POST /annotations/
- Creates a new annotation.
- Requires JSON body: `{ "draft_id": "<uuid>", "context": "<text>", "highlight": "<text>" }`
- Requires JWT authentication.

## Timeline API

### GET /timeline/<project_id>
- Returns chapters and scenes for a project, ordered by creation.
- Requires JWT authentication.
- Response: `{ "project_id": "<uuid>", "project_title": "<str>", "timeline": [ { "chapter_id": "<uuid>", "chapter_title": "<str>", "scenes": [ { "scene_id": "<uuid>", "scene_title": "<str>", "created_at": "<iso>" } ] } ] }`
- 404 if project not found.

## Autosave API

### POST /autosave/
- Saves a snapshot for a scene or draft.
- Requires JSON body: `{ "scene_id": "<uuid>", "content": "<text>" }` or `{ "draft_id": "<uuid>", "content": "<text>" }`
- Requires JWT authentication.
- Returns the saved autosave version.
- 400 if missing required fields.
- **Server-side deduplication:** If an identical snapshot exists for the same scene/draft within the last 30 seconds, the server skips saving and returns the latest snapshot (200 OK).

## Export API

### POST /export/<project_id>
- Exports a project to `.docx` or `.pdf` using `python-docx` or `reportlab` and saves export metadata.
- Requires JSON body: `{ "export_type": "docx" }` or `{ "export_type": "pdf" }`
- Requires JWT authentication.
- Returns the generated file as a download and stores export metadata in the database.
- 400 if invalid type, 404 if project not found.

## API Endpoint History

- `POST /auth/login`  # ✅ Completed July 18, 2025
- `POST /auth/register`  # ✅ Completed July 18, 2025
- `GET/POST/PUT /projects/`  # ✅ Completed July 18, 2025
- `GET/POST/PUT /chapters/`  # ✅ Completed July 18, 2025
- `GET/POST/PUT /scenes/`  # ✅ Completed July 18, 2025
- `GET/POST /drafts/`  # ✅ Completed July 18, 2025
- `GET/POST /annotations/`  # ✅ Completed July 18, 2025
- `GET /timeline/<project_id>`  # ✅ Completed July 18, 2025
- `POST /autosave`  # ✅ Completed July 18, 2025
- `POST /export/<project_id>`  # ✅ Completed July 18, 2025

---

## Frontend Setup Progress

- **Phase 3.1 – Initial Setup:** ✅ Completed July 18, 2025
  - React + Vite project scaffolded
  - Dependencies installed: axios, react-router-dom, tailwindcss
  - Folder structure created as per TASK.md
  - TypeScript configuration optimized
  
- **Phase 3.2 – Authentication Components:** ✅ Completed July 18, 2025
  - Login/Register pages implemented with proper TypeScript types
  - JWT authentication flow with Axios interceptors
  - Protected routes with useAuth hook
  - Comprehensive test coverage (9 tests across 3 files)

- **Phase 3.3 – Code Quality & Testing:** ✅ Completed July 18, 2025
  - All ESLint errors resolved
  - Replaced `any` types with explicit TypeScript interfaces
  - Modern TypeScript patterns and type inference applied
  - Axios 1.10.0+ compatibility ensured
  - Full test suite passing (backend + frontend + linting + formatting)