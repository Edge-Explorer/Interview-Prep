# 🎮 Technical Simulation & Session Flow: The Master Blueprint

This document outlines the architecture for the **Technical Coding Rounds**, **AI Judging System**, and the **Progression Game Loop** for InterviewAI.

---

## 🏗️ 1. The "LeetCode" Intelligence (Problem Sourcing)
Instead of generic questions, the system generates company-specific technical challenges.

*   **Source**: Integrated with the **Agentic Discovery System**.
*   **Contextual Generation**: 
    *   If the company is **Groq**, the problem focuses on *Hardware-aware software optimization* or *Parallel Array processing*.
    *   If the company is **OpenAI**, the focus shifts to *Transformer attention mechanisms* or *Vector search optimizations*.
*   **Format**: The AI provides a detailed Problem Statement, Sample Inputs/Outputs, and a "Bar" (Expert-level criteria).

## 🖥️ 2. The Coding Sandbox & AI Judge (Execution Layer)
We utilize a high-performance simulation model for code evaluation without the overhead of heavy containerization.

*   **The Sandbox (Frontend)**: Implemented using **Monaco Editor** (VS Code Engine) for a premium, developer-first experience.
*   **Option B: The AI Judge (Selected)**:
    *   **Mechanism**: The user's code is sent to the **Llama-3/Gemini** backend.
    *   **Verification**: The AI "Dry Runs" the code against the hidden test cases.
    *   **Evaluation Metrics**:
        1.  **Correctness**: Does it solve the logical core?
        2.  **Complexity**: Is the Time/Space complexity optimal for that specific company’s standard?
        3.  **Code Quality**: Readability, variable naming, and "Role Readiness" (e.g., SDE-1 vs Senior).

## 📈 3. The "Level-Up" Progression (The Game Loop)
The interview follows a strict **Gated Entry** flow to simulate a real high-stakes hiring process.

*   **Round Locking**: Round 1 (Technical) must be cleared with a score of **>70%** to unlock Round 2.
*   **Session State**: Managed via **Neon Cloud (PostgreSQL)** tracking `current_round`, `round_status`, and `accumulated_feedback`.
*   **The Gatekeeper**: A backend service that checks the AI Judge's verdict before updating the user's progress.

## 🧬 4. Role-Specific Logic (AI/ML vs SDE)
The "Bar" for passing varies significantly based on the user's target role:

| Role Category | Technical Focus | AI Judge Weighting |
| :--- | :--- | :--- |
| **SDE / Backend** | DS & Algorithms, System Latency | Efficiency, Edge Cases |
| **AI/ML Engineer** | Array Math (NumPy), Optimization | Mathematical Logic, Data flow |
| **GenAI Developer** | Prompt patterns, RAG logic, Vector DBs | Pattern recognition, Semantic understanding |

## 🛠️ 5. The "Fail" Branch (The Learning Roadmap)
Failure is transformed into an opportunity for growth.

*   **Post-Mortem**: If a user fails a round, the **Learning Roadmap Agent** is triggered.
*   **Personalization**: It analyzes the specific mistakes in the code and generates a **7-Day Study Plan** targeted at the user's weak points.
*   **Infinite Loop**: Once the user completes the roadmap, they can "Re-attempt" the high-fidelity simulation.

---

## ✅ Implementation Status Note

> **Previously**: This document contained a "Loophole Warning" blocking implementation of the Coding Round system.
>
> **Resolved (February 2026)**: The loophole has been addressed. The full Coding Round solution — including **Whiteboard Mode**, **AI Dry Run**, **Tiered Hint System**, **JSON Learning Ledger**, and the **Persona Architecture** — is now designed and documented in:
>
> 📄 [`CODING_ROUND_DESIGN.md`](./CODING_ROUND_DESIGN.md)
>
> Implementation begins in the next sprint (Phase 6).
