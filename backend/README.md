# Backend - InterviewAI Core

This directory contains the FastAPI-based backend for the InterviewAI platform. It handles authentication, interview session management, AI question generation via Gemini, and result evaluation.

## 📂 File Structure & Responsibilities

| File | Purpose |
|------|---------|
| `main.py` | The main entry point. Sets up FastAPI, middleware (CORS), and all API endpoints (`/auth`, `/interviews`, `/users`). |
| `models.py` | SQLAlchemy database models. Defines the schema for `User`, `InterviewSession`, `Payment`, and `LearningRoadmap`. |
| `schemas.py` | Pydantic models for request/response validation. Ensures data integrity across the API. |
| `database.py` | Database connection logic using SQLAlchemy and SQLite. |
| `auth_utils.py` | Security helpers: password hashing, JWT token generation, and user authentication dependency. |
| `round_config.py` | Configuration for interview rounds (Technical, Behavioral, HR, etc.) including specific focus areas. |
| `services/` | Contains external integrations like the AI service. |

## 🚀 Key Features
1. **AI Interviewer**: Integrated with Google Gemini API to generate real-time, adaptive questions.
2. **Contextual Analysis**: Processes PDF resumes to tailor interview topics to the user's specific background.
3. **Session Management**: Tracks interview progress across multiple rounds (Technical, HR, etc.).
4. **Automated Evaluation**: AI-driven scoring system that provides "Honest Recruiter Feedback" and determines if a candidate can proceed.

## 🛠 Tech Stack
- **Framework**: FastAPI (Python)
- **Database**: SQLite (SQLAlchemy)
- **AI**: Google Gemini Pro (Generative AI)
- **Auth**: JWT (JSON Web Tokens)
- **PDF Parsing**: PyPDF
