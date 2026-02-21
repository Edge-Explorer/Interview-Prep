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

4. **`round_config.py`** *(v2.3 — Domain-Aware Round Engine)*:
    - Defines `ROUND_DEFINITIONS` — all 12 round types (Technical, System Design, Case Study, Situational, Role Play, Portfolio Review, Practical Assessment, Technical Presentation, Behavioral, Managerial, Final) with min/max questions and pass score thresholds.
    - Defines `DOMAIN_ROUND_SEQUENCES` — each of the 12 career domains gets its own ordered round sequence per difficulty level (Junior / Mid / Senior). Finance & Accounting, Legal, and Business get `Case Study`. Healthcare gets `Situational`. Creative gets `Portfolio Review`. Engineering & Tech gets `System Design`. All domains get `Managerial` at Senior level.
    - Exposes `get_first_round()`, `get_next_round()`, `get_round_config()`, `should_proceed_to_next_round()` helpers used by `main.py`.
