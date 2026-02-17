# Backend - InterviewAI Core

**Architected & Authored by: [Karan Shelar](https://github.com/Edge-Explorer)**

This directory contains the FastAPI-based backend for the InterviewAI platform. It handles authentication, interview session management, AI question generation via Gemini, company-specific interview intelligence, and result evaluation.

## 📂 File Structure & Responsibilities

| File/Directory | Purpose |
|----------------|---------|
| `main.py` | The main entry point. Sets up FastAPI, middleware (CORS), and all API endpoints (`/auth`, `/interviews`, `/users`). |
| `models.py` | SQLAlchemy database models. Defines the schema for `User`, `InterviewSession`, `Payment`, and `LearningRoadmap`. |
| `schemas.py` | Pydantic models for request/response validation. Ensures data integrity across the API. |
| `database.py` | Database connection logic using SQLAlchemy and Neon PostgreSQL. |
| `auth_utils.py` | Security helpers: password hashing, JWT token generation, and user authentication dependency. |
| `round_config.py` | Configuration for interview rounds (Technical, Behavioral, System Design, Managerial, Final). |
| **`services/`** | **External integrations and intelligence services** |
| `services/gemini_service.py` | Google Gemini AI integration for question generation and evaluation. |
| `services/company_intelligence.py` | Company intelligence service with curated database lookup. |
| `services/intelligence_service.py` | **ACTIVE**: Agentic multi-agent workflow using LangGraph for real-time research. |
| **`interview_ai_model/`** | Fine-Tuned Llama-3 LoRA adapters (Excl. from Git). |
| **`data/`** | **Static data and intelligence databases** |
| `data/company_profiles.json` | Curated database of 383 unique companies across 12 domains. |
| `data/discoveries.json` | **NEW**: Memory layer for dynamically discovered company profiles. |
| `test_intelligence_agent.py` | Test script to verify the LangGraph Agentic Brain functionality. |

## 🚀 Key Features

1. **AI Interviewer**: Integrated with Google Gemini 2.0 Flash API to generate real-time, adaptive questions.
2. **Company Intelligence System (v2.1)**: 
   - **Tier 1 (Curated)**: Expert intelligence for **383 companies** (100% offline).
   - **Tier 2 (Agentic Discovery)**: Live research via **DuckDuckGo** for any unknown company.
   - **Tier 3 (Permanent Memory)**: Discovered companies are saved to `discoveries.json` for zero-latency future access.
   - **The Brain**: Orchestrated by LangGraph (Researcher, Architect, Critic agents).
3. **Contextual Analysis**: Processes PDF resumes to tailor interview topics to the user's specific background.
4. **Cloud-Ready Infrastructure**: Fully integrated with **Neon PostgreSQL** for serverless, cloud-side data storage.
5. **Multi-Round System**: Supports 5 interview rounds (Technical, Behavioral, System Design, Managerial, Final).

## 🛠 Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: Neon PostgreSQL (SQLAlchemy ORM + Alembic)
- **Agents**: LangGraph + LangChain
- **Search**: duckduckgo-search (DDGS)
- **AI**: Google Gemini 2.0 Flash & Fine-Tuned Llama-3-8B
- **Auth**: JWT with SHA-256 + Bcrypt double-hashing

## 🏢 Intelligence Database Coverage (383 Companies)

The system features at least **20 companies** in every single category:

- 🔹 **Engineering & Tech**: 134 companies (FAANG, SaaS, AI, etc.)
- 🔹 **Business & Management**: 23 companies (Staffing, HR, Business)
- 🔹 **Construction & Trades**: 23 companies (Heavy Engineering, Infra)
- 🔹 **Social Services**: 23 companies (Non-profits, Foundations)
- 🔹 **Finance & Accounting**: 22 companies (Fintech, Banking, Trading)
- 🔹 **Healthcare & Medical**: 22 companies (Biotech, Pharma, Health IT)
- 🔹 **Legal**: 22 companies (Law firms, Legal Tech)
- 🔹 **Science & Research**: 22 companies (Research Labs, Space)
- 🔹 **Hospitality & Tourism**: 21 companies (Travel, Food, Booking)
- 🔹 **Creative & Design**: 21 companies (Media, Animation, VFX)
- 🔹 **Education & Training**: 21 companies (EdTech, Universities)
- 🔹 **Sales & Marketing**: 20 companies (Advertising, Market Research)

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
