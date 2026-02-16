# Backend - InterviewAI Core

**Architected & Authored by: [Karan Shelar](https://github.com/Edge-Explorer)**

This document outlines the strategic plan for evolving InterviewAI from a static database into a self-learning, agentic intelligence system.

## 🏁 Phase 1: Custom Model Fine-Tuning (Completed)
- **Status**: ✅ Milestone Reached (Feb 2026)
- **Action**: Fine-tuned **Llama-3-8B** using the **Unsloth** library on a dataset of 383 curated company profiles.
- **Results**: The model (LoRA Adapters) now internalizes the structural requirements of our platform, including interview styles, rounds, and cultural value formatting. Loss reduced from **1.93 to 0.22**.

## 🚀 Phase 2: The Agentic Workflow (Current Goal)
We are moving away from simple "Request-Response" logic to a **state-machine based agent workflow** using **LangGraph**. This reduces hallucinations and ensures 99% data accuracy.

### 🛡️ What is an Agentic Workflow?
Unlike a standard chatbot that answers instantly (and often guesses), an agentic workflow follows a logical path of "Nodes." Each node has a specific job and can "double-check" the previous one.

### 🗺️ The LangGraph Node Map:
1. **NODE: The Gatekeeper (Classifier)**
   - Check if the requested company exists in `company_profiles.json`.
   - If **FOUND**: Serve instantly from the local database.
   - If **NOT FOUND**: Trigger the "Research Agent."

2. **NODE: The Researcher (Fact Finder)**
   - Use **DuckDuckGo Search** (via LangChain-Community) or Gemini's internal high-speed memory.
   - Extract industry, recent news, mission statement, and key products.

3. **NODE: The Architect (Fine-Tuned Llama-3)**
   - Take the "messy" facts from the Researcher.
   - Pass them through our **Fine-tued LoRA Adapters**.
   - Generate a perfectly structured JSON profile that matches our project's exact schema.

4. **NODE: The Critic (Validator)**
   - Use a light Gemini model to "Review" the JSON.
   - Check for: valid JSON syntax, logical consistency (e.g., a "Retail" company shouldn't have "Embedded Systems" rounds).
   - If errors found: Loop back to The Architect for one correction.

5. **NODE: The Persona Injector (Adinath/Veda)**
   - Final transformation. Wrap the data in the specific personality of the selected interviewer.

## 🔄 Phase 3: The Infinite Learning Loop
- **Objective**: Zero-Manual-Work Expansion.
- **Logic**: Any high-quality profile generated for an "Unknown" company is automatically saved to a `discoveries.json` file.
- **Growth**: Every few months, we run one "Expansion Merge" to add these new discoveries into the main database, increasing our "Curated" list from 383 to 1,000+ companies for free.

## 🛠️ Tech Stack for this Plan
- **Orchestration**: LangGraph (for complex state logic).
- **Tooling**: LangChain (for tool calling and search wrappers).
- **Core Brain**: Gemini 2.0 Flash (Free/Low-cost logic).
- **Style Brain**: Custom Llama-3 Fine-Tuned (High-fidelity structure).
- **Storage**: JSON-based local persistence + Hugging Face backups.

---
*Document Version: 1.0.0*
*Developer: Student-Friendly, High-Performance Architecture Plan*
