# Writer Tool Backend

Flask-based REST API for the Writer & Screenwriter Tool project.

## 🚀 Quick Start

### Option 1: Docker (Recommended)
```bash
# Start all services
docker-compose up --build

# The API will be available at http://localhost:5000
```

### Option 2: Local Development
```bash
# Run the setup script
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Copy environment file
cp .env.example .env
# Edit .env with your configuration

# Start PostgreSQL (you need PostgreSQL running locally)
# Then run the Flask app
python run.py
```

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user info

### Projects
- `GET /api/projects/` - List user projects
- `POST /api/projects/` - Create new project
- `GET /api/projects/{id}` - Get specific project
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

### Chapters
- `POST /api/chapters/` - Create new chapter
- `GET /api/chapters/{id}` - Get specific chapter
- `PUT /api/chapters/{id}` - Update chapter
- `DELETE /api/chapters/{id}` - Delete chapter

### Scenes
- `POST /api/scenes/` - Create new scene
- `GET /api/scenes/{id}` - Get specific scene
- `PUT /api/scenes/{id}` - Update scene
- `DELETE /api/scenes/{id}` - Delete scene
- `POST /api/scenes/{id}/toggle-draft` - Toggle draft mode

### Autosave
- `POST /api/autosave/` - Create autosave backup
- `GET /api/autosave/{project_id}/versions` - Get autosave versions

### Exports
- `POST /api/exports/{project_id}` - Export project (DOCX/PDF)

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models/              # Database models
│   │   ├── __init__.py      # Base model
│   │   ├── user.py          # User model
│   │   ├── project.py       # Project model
│   │   ├── chapter.py       # Chapter model
│   │   ├── scene.py         # Scene model
│   │   ├── annotation.py    # Annotation model
│   │   ├── export.py        # Export model
│   │   └── autosave.py      # Autosave model
│   ├── routes/              # API routes
│   │   ├── auth.py          # Authentication routes
│   │   ├── projects.py      # Project CRUD
│   │   ├── chapters.py      # Chapter CRUD
│   │   ├── scenes.py        # Scene CRUD
│   │   ├── exports.py       # Export functionality
│   │   └── autosave.py      # Autosave functionality
│   ├── services/            # Business logic
│   └── utils/               # Utility functions
├── migrations/              # Database migrations
├── tests/                   # Test files
├── config.py               # Configuration settings
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker container config
├── docker-compose.yml     # Multi-container setup
└── .env.example           # Environment variables template
```

## 🔧 Development

### Database Migrations
```bash
# Initialize migrations (first time only)
flask db init

# Create a new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade
```

### Testing
```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py
```

### Code Quality
```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .
```

## 🔐 Authentication

All API endpoints (except auth) require a JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## 📊 Database Schema

The application uses PostgreSQL with the following main entities:
- **Users**: Authentication and profile information
- **Projects**: Top-level writing projects (books, scripts)
- **Chapters**: Major sections within projects
- **Scenes**: Individual writing units within chapters
- **Annotations**: Text highlights and notes
- **Exports**: Export history and metadata
- **AutosaveVersions**: Automatic backup snapshots

## 🐳 Docker Services

- **backend**: Flask API server
- **db**: PostgreSQL database
- **redis**: Redis cache (for future use)

## 📝 Next Steps

1. **Models Implementation** - Create SQLAlchemy models (Phase 2.2)
2. **Authentication** - Implement JWT auth system (Phase 2.3)
3. **Export Functionality** - Add DOCX/PDF generation (Phase 2.6)
4. **Testing** - Add comprehensive test suite (Phase 2.7)

---

For the complete project documentation, see the main README.md file.
