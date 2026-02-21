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
- **Validated** System performance against real-world firms (e.g., Idolize Business Solutions, Mistral AI).
- **Implemented** Source Attribution: The AI now captures and links all research sources in the final profile.
- **Implemented** Evergreen Temporal Search: Upgraded the Researcher to dynamically calculate years for perpetual freshness.
- **Implemented** The Auditor Agent (The Bouncer): A dedicated node that filters 'Vomit' (noise like Vastu/NCERT), verifies Company Identity vs Job Description, and generates an 'Audit Log' for developer transparency.
- **Fixed** Information Starvation Bug: Upgraded the Researcher/Auditor nodes to preserve and pass full search metadata (Title + Body). This slashed hallucinations and fixed the "Confidence 0" issue for rare companies.
- **Implemented** Domain Guard (Role-Company Logic): Added a contextual cross-check to the Auditor and Architect nodes. The system now detects mismatches between the user's role (e.g., Software Engineer) and the company's actual industry (e.g., Creative Agency), and provides a logical explanation of the alignment instead of hallucinating.
- **Improved** Validation Logic: Enforced strict Critic-based approval before any discovery is saved to `discoveries.json`, ensuring the memory stays pristine.
- **Updated** Comprehensive Documentation: Refactored root, backend, and discovery READMEs to reflect the new 4-agent architecture and Mermaid diagrams. Created `CHALLENGES.md` to document the project's complex technical solutions.
- **Fixed** Critical Data Integrity loophole: Implemented "Global Vault" isolation for Stealth/Synthetic data.
- **Fixed** Strict Identity Bug: Tightened fuzzy matcher threshold (95%) to prevent collisions.
- **Implemented** Dynamic Domain Intelligence (v2.2): Added logic to prevent 'Role Forcing' on non-tech companies (e.g., Clinical/Legal/Creative) during profile architecture.
- **Implemented** Geographic Guardrails: Built a location-aware `router_node` to prevent cross-continental naming collisions (e.g., MOC India vs Moffitt USA).
- **Implemented** Confidence Score System: Standardized confidence weighting (0-160) for clear Status/Reliability tracking.
- **Fixed** Memory Integrity: Recovered and cleaned `discoveries.json` after accidental malformed JSON writing; added a 98% fuzzy threshold for discovery memory retrieval.
- **Implemented** Audit Status: Added `ACCEPTED/REJECTED` status tracking in the Audit Log for every source link.

- **Implemented** Evergreen Perpetual Freshness (v2.2.2): Replaced hardcoded years (2025/2026) with dynamic temporal logic that auto-calculates current and future years for research queries.
- **Fixed** Mermaid Diagram Rendering Error: Quoted all special-character labels in the README architecture diagram so it renders correctly on GitHub (was throwing 'Parse error on line 10').
- **Refactored** Documentation Structure: Moved all loose root-level markdown files into a dedicated `/docs` folder using `git mv` (preserving history). Created a `docs/README.md` navigation index and a quick-link bar in the main README.
- **Designed** Coding Round Intelligence System (v3.0 Roadmap): Authored full 9-section blueprint (`CODING_ROUND_DESIGN.md`) covering Whiteboard Mode, AI Dry Run, Tiered Hints, JSON Learning Ledger, and Persona Architecture (Adinath vs. Veda).
- **Tested** Autonomous Discovery: Validated with companies including WABRIC, Aminuteman Technologies, and Shastra Solutions. Confirmed audit logs, source filtering, and confidence scores are working correctly.

### **Abhiraj**
- *Starting contributions today (tracking development from this point forward).*

---

## ✅ Major Version Milestones

| Feature / Update | Version | Status | Key Highlights |
| :--- | :--- | :--- | :--- |
| **Coding Round Intelligence Design** | v3.0 (Planned) | 🚧 In Progress | Whiteboard Mode, AI Dry Run, Tiered Hints, Learning Ledger. |
| **Docs Reorganization** | v2.2.2 | ✅ Done | All docs moved to `/docs` folder. Nav bar added to README. |
| **Mermaid Diagram Fix** | v2.2.2 | ✅ Done | Fixed GitHub parse error by quoting all special node labels. |
| **Evergreen Perpetual Freshness** | v2.2.2 | ✅ Done | Dynamic `datetime` year anchoring — no more hardcoded years. |
| **Geographic Guardrails** | v2.2.1 | ✅ Done | Location-aware routing to stop name collisions. |
| **Dynamic Domain Guard** | v2.2.1 | ✅ Done | Prevents forcing tech rounds on non-tech firms. |
| **Public Deployment** | v3.0 (Planned) | 🔮 Not Started | Backend (Render/AWS Lambda) + Frontend (Vercel) — planned. |
| **Agentic Intelligence Brain** | v2.1.0 | ✅ Done | Integrated LangGraph Researcher-Architect team. |
| **Stealth Mode Logic** | v2.1.0 | ✅ Done | AI now reverse-engineers JD for private startups. |
| **Neon Cloud PostgreSQL** | v2.1.0 | ✅ Done | Cloud-hosted database connected for sessions and users. |
| **398 Company Profiles** | v2.1.0 | ✅ Done | Pre-loaded intelligence database across 12 domains. |
| **ATS Resume Analysis** | v2.0.0 | ✅ Done | Gemini-powered PDF parsing and matching. |
| **Persona System** | v1.5.0 | ✅ Done | Created Adinath & Veda simulation personalities. |

---

## 🛠️ Contribution Guidelines
- **Branches**: Create a feature branch for every major update.
- **Commits**: Use descriptive messages (e.g., `feat: add stealth mode logic`).
- **Sync**: Always run `alembic upgrade head` after pulling changes.
