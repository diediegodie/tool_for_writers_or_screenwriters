# Writer & Screenwriter Tool

A productivity and structure management tool for writers and screenwriters. Organize your work into projects, chapters, and scenes. Write, annotate, save automatically, and export with ease.

## Tech Stack

**Frontend**
- React (Vite)
- Slate.js or Quill.js
- TailwindCSS
- Axios

**Backend**
- Flask (Python)
- PostgreSQL + SQLAlchemy
- JWT Authentication
- DOCX + PDF export

**Infrastructure**
- Docker + Docker Compose
- GitHub Actions (CI/CD)

---


# Backend testing uses pytest and pytest-flask. All models, routes, and export logic are covered by unit and integration tests. Tests run in an isolated SQLite database and can be executed from the project root with `pytest`. All tests passing as of July 18, 2025.

---

## Drafts API

### GET /drafts/
- Returns a list of all drafts.
- Requires JWT authentication.

### POST /drafts/
- Creates a new draft.
- Requires JSON body: `{ "scene_id": "<uuid>", "content": "<text>" }`
- Requires JWT authentication.

## Annotations API

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