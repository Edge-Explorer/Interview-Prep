# 👥 Project Collaborators

This document tracks the core team and the implementation history of the **InterviewAI** project.

---

## 🏗️ Core Development Team

| Name | Role | Focus |
| :--- | :--- | :--- |
| **Karan Shelar** | Lead Architect | AI Systems, LangGraph orchestration, Full-Stack Development |
| **Abhiraj** | Collaborator | Full-Stack Development (Backend & Frontend), System Refinement |

---

## 📝 Activity & Implementation Log

This section is for tracking specific task completions and problem-solving history.

### **Karan**
- **Implemented** Agentic Discovery System using LangGraph (Researcher-Architect-Critic).
- **Implemented** Stealth Mode logic with JD reverse-engineering for unknown companies.
- **Implemented** Neon Cloud PostgreSQL migration and production database sync.
- **Implemented** Massive company intelligence database (383+ profiles).
- **Implemented** Universal Gemini evaluation logic with company-context integration.
- **Implemented** Zero-Hallucination Framework: Integrated Critic Grounding, Trust Score system (0-100), and "I Don't Know" Policy to prevent AI imagination.
- **Implemented** Optimization Suite: Added `rapidfuzz` for better matching, refined DDGS queries for noise reduction, and a "Status Stream" for latency feedback.
- **Fixed** Logic bug in Agentic Discovery where naming conflicts (name vs company_name) prevented saving to `discoveries.json`.

### **Abhiraj**
- *Starting contributions today (tracking development from this point forward).*

---

## ✅ Major Version Milestones

| Feature / Update | Version | Status | Key Highlights |
| :--- | :--- | :--- | :--- |
| **Agentic Intelligence Brain** | v2.1.0 | Done | Integrated LangGraph Researcher-Architect team. |
| **Stealth Mode Logic** | v2.1.0 | Done | AI now reverse-engineers JD for private startups. |
| **Neon Cloud Sync** | v2.1.0 | Done | Migrated DB to Serverless PostgreSQL (Neon). |
| **383+ Company Profiles** | v2.1.0 | Done | Massive pre-loaded intelligence database. |
| **ATS Resume Analysis** | v2.0.0 | Done | Gemini-powered PDF parsing and matching. |
| **Persona System** | v1.5.0 | Done | Created Adinath & Veda simulation personalities. |

---

## 🛠️ Contribution Guidelines
- **Branches**: Create a feature branch for every major update.
- **Commits**: Use descriptive messages (e.g., `feat: add stealth mode logic`).
- **Sync**: Always run `alembic upgrade head` after pulling changes.
