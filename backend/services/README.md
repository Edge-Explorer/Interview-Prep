# Backend Services - AI Integration

This directory houses the logic for interacting with external AI providers and automated services.

## 📂 Core Service: Gemini AI (`gemini_service.py`)

The `GeminiService` class is the "brain" of InterviewAI. It manages all interactions with the Google Gemini API.

### Key Capabilities:
1. **Resume Analysis**:
    - Parses PDF content.
    - Extracts key projects, skills, and experience levels.
    - Builds a "Candidate Profile" for the AI interviewer.

2. **Adaptive Questioning**:
    - Tailors questions based on the `role_category` (e.g., Tech, Finance) and `difficulty_level`.
    - Implements specific personas: **Adinath** (Technical/Logic focus) and **Veda** (HR/Behavioral focus).

3. **Intelligent Evaluation**:
    - Analyzes candidate responses using the context of the previous question.
    - Provides a score from 1-10.
    - Generates constructive, "honest" feedback from a mock recruiter's perspective.

### Security Note
- Uses the `GEMINI_API_KEY` stored in the root `.env` file.
- Prompt engineering is used to restrict the AI to professional interview behavior.

## 🏢 Intelligence Services

### 1. `company_intelligence.py`
The "Quick Lookup" service. It manages the curated **402-company** database. It uses fuzzy matching to find companies regardless of typos or naming variations (e.g., "FB" vs "Facebook").

### 2. `intelligence_service.py` (The LangGraph Brain - v2.3)
The "Autonomous Discovery" service. Used when a company is not in the curated DB.
- **Node-Based Architecture**:
    - **Router**: Detects ambiguity, location, and industry (Geographic Guarding).
    - **Researcher**: Scrapes DuckDuckGo for live facts. Applies a **Python-Level Domain Blocklist** (14 generic SEO article domains e.g. datacamp, guru99) to purge junk *before* it reaches the AI.
    - **Auditor**: Filters noise and applies **Dynamic Domain Guarding** (prevents 'Role Forcing').
    - **Architect**: Generates a structured profile (Llama-3/Gemini).
    - **Critic**: Reflects and corrects the profile for quality.
- **Identity Guarding**: Uses a strict **98% fuzzy matching threshold** to prevent name collisions in memory.
- **Permanent Memory**: Automatically saves approved profiles to `discoveries.json`.
