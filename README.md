# Aushadh Vigil Backend

This is the backend for the Aushadh Vigil platform – a lightweight web service that predicts and explains interactions between Ayurvedic medicines and modern pharmaceutical drugs.

## Setup

1. Clone the repository.
2. Navigate to the `backend` directory.
3. Create a Python virtual environment (if not already created):
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Copy `.env.example` to `.env` and adjust values as needed.
6. Apply database migrations (Alembic):
   ```bash
   alembic upgrade head
   ```
7. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000` with interactive docs at `/docs`.

## Project Structure

```
backend/
├─ app/
│  ├─ main.py              # FastAPI app creation and router inclusion
│  ├─ config.py            # Pydantic settings loading from .env
│  ├─ db/
│  │  ├─ base.py           # SQLAlchemy declarative base
│  │  ├─ session.py        # Async engine and session factory
│  │  └─ models/           # ORM models (Herb, Drug, Interaction, etc.)
│  ├─ api/
│  │  └─ v1/
│  │     └─ routers/       # Versioned API routers (herbs, drugs, predict, etc.)
│  ├─ services/            # Business logic (interaction, explanation, literature, PDF)
│  ├─ utils/               # Helper functions
│  └─ migrations/          # Alembic migration scripts
├─ models/                 # Persisted ML model artifacts (pickle, ONNX, etc.)
├─ tests/                  # Test suites
├─ requirements.txt        # Python dependencies
├─ .env.example            # Template environment variables
└─ README.md               # This file
```

## License

[Specify license if any]
