# 🏗️ Core Infrastructure - Database & Models

This directory defines the foundational data structures and database configuration for the entire application.

## 📂 Key Components

1. **`models.py`**:
    - Defines the SQLAlchemy ORM models (Users, Interviews, Payments, roadmaps).
    - Handles relationships and data hierarchy.

2. **`database.py`**:
    - Manages the engine connection to Neon Cloud (PostgreSQL).
    - Provides the `get_db()` session dependency for FastAPI.

3. **`schemas.py`**:
    - Contains the Pydantic models for request/response validation.
    - Ensures type safety across the API.

4. **`round_config.py`**:
    - Stores the configuration for interview rounds (e.g., number of questions per round).
