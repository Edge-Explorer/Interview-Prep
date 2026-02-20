# Backend - InterviewAI Core

**Architected & Authored by: [Karan Shelar](https://github.com/Edge-Explorer)**

This directory contains the FastAPI-based backend for the InterviewAI platform. It handles authentication, interview session management, AI question generation via Gemini, company-specific interview intelligence, and result evaluation.

## 📂 File Structure & Responsibilities

| File/Directory | Purpose |
|----------------|---------|
| `main.py` | The main entry point. Sets up FastAPI and all API endpoints. |
| **`core/`** | **Foundational logic**: `database.py`, `models.py`, `schemas.py`, `round_config.py`. |
| **`auth/`** | **Security**: Authentication utilities and token management. |
| **`services/`** | **Intelligence**: Gemini, Agentic Researcher, and Curated Intelligence. |
| **`tests/`** | **Verification**: All automated test cases and GPU diagnostics. |
| **`scripts/`** | **Maintenance**: Utility scripts for DB management and data entry. |
| **`data/`** | **Knowledge**: `company_profiles.json`, `discoveries.json`, and training data. |
| **`interview_ai_model/`** | Fine-Tuned Llama-3 LoRA adapters (Excl. from Git). |

## 🚀 Key Features

1. **AI Interviewer**: Integrated with Google Gemini 2.0 Flash API to generate real-time, adaptive questions.
2. **Company Intelligence System (v2.2.1)**: 
   - **Tier 1 (Curated)**: Expert intelligence for **383 companies** (100% offline).
   - **Tier 2 (Agentic Discovery)**: Live research via **DuckDuckGo** with **Evergreen Perpetual Freshness** (Auto-calculating Current Year).
   - **Dynamic Domain Intelligence**: Automatically prevents "Role Forcing" in non-tech industries.
   - **Geographic Guarding**: Dedicated router node to prevent cross-continental name collisions.
   - **The Auditor (The Bouncer)**: Dedicated node that purges noise and verifies JD/Identity alignment.
   - **Tier 3 (Stealth Mode)**: AI reverse-engineers company culture from the user's **JD**.
   - **Tier 4 (Synthetic Logic)**: Industry-standard fallback with strict Identity Guarding (98% threshold).
   - **The Brain**: Orchestrated by a 5-agent LangGraph team (Router-Researcher-Auditor-Architect-Critic).

### 🛠️ Confidence & Reliability Matrix
| Score | Meaning | Logic |
| :--- | :--- | :--- |
| **0 - 20** | **Synthetic** | Fallback to industry-standard benchmarks. |
| **85** | **Verified** | Successful research + identity verification. |
| **100+** | **Elite Certified** | Multi-source verification + location/industry match. |
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

Run the Agentic Intelligence test:
```bash
.\venv\Scripts\python tests\test_intelligence_agent.py "Google"
```

Run fuzzy matching benchmarks:
```bash
.\venv\Scripts\python tests\test_fuzzy_matching.py
```
