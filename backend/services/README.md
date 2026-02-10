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
- Prompt engineering is used to restrict the AI to professional interview behavior and prevent system leakage.
