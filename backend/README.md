# Backend - InterviewAI Core

This directory contains the FastAPI-based backend for the InterviewAI platform. It handles authentication, interview session management, AI question generation via Gemini, company-specific interview intelligence, and result evaluation.

## 📂 File Structure & Responsibilities

| File/Directory | Purpose |
|----------------|---------|
| `main.py` | The main entry point. Sets up FastAPI, middleware (CORS), and all API endpoints (`/auth`, `/interviews`, `/users`). |
| `models.py` | SQLAlchemy database models. Defines the schema for `User`, `InterviewSession`, `Payment`, and `LearningRoadmap`. |
| `schemas.py` | Pydantic models for request/response validation. Ensures data integrity across the API. |
| `database.py` | Database connection logic using SQLAlchemy and SQLite. |
| `auth_utils.py` | Security helpers: password hashing, JWT token generation, and user authentication dependency. |
| `round_config.py` | Configuration for interview rounds (Technical, Behavioral, System Design, Managerial, Final) including specific focus areas and pass scores. |
| **`services/`** | **External integrations and intelligence services** |
| `services/gemini_service.py` | Google Gemini AI integration for question generation and evaluation. |
| `services/company_intelligence.py` | **NEW**: Company-specific interview intelligence service with curated database. |
| **`data/`** | **Static data and intelligence databases** |
| `data/company_profiles.json` | **NEW**: Curated database of 11+ top companies with interview styles, cultural values, and round-specific intelligence. |
| `test_company_intel.py` | Test script to verify Company Intelligence System functionality. |

## 🚀 Key Features

1. **AI Interviewer**: Integrated with Google Gemini 2.0 Flash API to generate real-time, adaptive questions.
2. **Company Intelligence System (NEW)**: 
   - **Tier 1 (Curated)**: Rich, company-specific interview intelligence for 11+ top companies (Google, Amazon, Microsoft, Meta, Apple, Netflix, Uber, Airbnb, Stripe, Salesforce, Adobe)
   - **Tier 3 (AI Fallback)**: Uses Gemini's general knowledge for companies not in database
   - Includes cultural values, interview styles, common topics, and red flags
3. **Contextual Analysis**: Processes PDF resumes to tailor interview topics to the user's specific background.
4. **Multi-Round System**: Supports 5 interview rounds (Technical, Behavioral, System Design, Managerial, Final) with role-based applicability.
5. **Session Management**: Tracks interview progress across multiple rounds with round-specific scoring.
6. **Automated Evaluation**: AI-driven scoring system that provides "Honest Recruiter Feedback" and determines if a candidate can proceed to the next round.

## 🛠 Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL (SQLAlchemy ORM)
- **AI**: Google Gemini 2.0 Flash (Generative AI)
- **Auth**: JWT (JSON Web Tokens) with SHA-256 + Bcrypt hashing
- **PDF Parsing**: PyPDF
- **Company Intelligence**: JSON-based curated database (100% free, no API calls)

## 🏢 Company Intelligence Database

The system includes curated interview intelligence for:
- **FAANG**: Google, Amazon, Meta, Apple, Netflix
- **Tech Giants**: Microsoft, Uber, Salesforce, Adobe
- **High-Growth**: Stripe, Airbnb

Each company profile includes:
- Interview style (technical-heavy, culture-fit-heavy, etc.)
- Cultural values and leadership principles
- Round-specific focus areas and common topics
- Interview tips and red flags
- Average process duration

## 🧪 Testing

Run the Company Intelligence test:
```bash
python test_company_intel.py
```

This verifies:
- Company profiles are loaded correctly
- Case-insensitive matching works
- Tier 1 (curated) vs Tier 3 (fallback) logic
- Cultural values and interview context generation
