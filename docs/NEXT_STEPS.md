# 🚀 The Journey Ahead: Next Steps

This document outlines the strategic roadmap and upcoming technical features for **InterviewAI**.

> **Current Version**: v2.2.2 | **Last Updated**: February 2026

---

## 🔥 Immediate Priority (Next 2–3 Days)

### 🧠 Phase 6: Coding Round Intelligence
*Full design spec: [`CODING_ROUND_DESIGN.md`](./CODING_ROUND_DESIGN.md)*

- [ ] **Day 1 — Backend Brain**: Build Problem Spec Generator, AI Dry Run Engine, and `/interview/coding-submit` + `/interview/coding-log` endpoints.
- [ ] **Day 2 — Hint Engine + Personas**: Tiered Hint Generator, Adinath's Pressure Mode, Veda's Verbalization Gate, and Resume Hook Extractor.
- [ ] **Day 3 — Frontend Whiteboard UI**: Split-pane editor + Persona toggle + Post-Round Code Review Report render.

---

## 🎯 Short-Term Goals (Next 2 Weeks)

### 1. ⚡ UI/UX "Agentic" Feedback
- [ ] Add a "Researcher at Work" animated terminal in the UI to show real-time agent activity.
- [ ] Show the user when the AI is in "Stealth Mode" vs "Public Research" mode with a visual indicator.
- [ ] Polish the `discoveries.json` visual rendering in the dashboard.

### 2. 🏆 Interview Flow Polish
- [ ] Implement a final "Hiring Decision" report after all 5 rounds are completed.
- [ ] Implement iterative difficulty scaling (Round 2 is harder if Round 1 was "Elite").

### 3. 🧠 Intelligence Refinement (Phase 2.5)
- [ ] **Cross-Continental Localization**: Enhance the Router to detect if a company has different processes (e.g., Google US vs Google India).
- [ ] **Discovery Dashboard**: Create a UI screen to browse the global `discoveries.json` database.
- [ ] **Real-time Search Streaming**: Push live research logs (ACCEPTED/REJECTED links) directly to the user's dashboard.
- [ ] **Automatic Memory Pruning**: Build a script to periodically "refresh" discoveries that are older than 6 months.

---

## 💡 Tech Debt & Maintenance

- [ ] Refine the "Critic" agent prompts to catch even more subtle hallucinations.
- [ ] Expand the Curated Database from 398 companies to 500+.
- [ ] Implement robust error handling and retry logic for DuckDuckGo rate limits (exponential backoff).

---

## 🏔️ Long-Term Vision (Future Roadmap)

### 📊 AI-Generated Learning Roadmaps
- Build the complete logic to transform interview feedback into a personalized 7-day study plan stored in the database, currently only the generator exists.

### 🎥 Video/Voice Integration
- Implement real-time WebRTC logic to analyze body language and tone during the session.

### 🏆 Community & Scores
- Create a global leaderboard for "Google-Level" readiness scores.
- Allow users to share their "Interview Intelligence Reports" on LinkedIn.

---

## ✅ Recently Completed (This Sprint)

- [x] **Mermaid Architecture Diagram** — Fixed parse error on GitHub. All node labels properly quoted.
- [x] **Docs Reorganization** — All loose markdown files moved to `/docs` folder with navigation index.
- [x] **Evergreen Perpetual Freshness (v2.2.2)** — Dynamic year calculation via `datetime`. No more hardcoded years.
- [x] **Geographic Guardrails** — Location-aware `router_node` prevents cross-continental name collisions.
- [x] **Domain Guard (v2.2)** — Prevents AI from forcing LeetCode rounds on non-tech companies.
- [x] **Supabase RLS** — Row Level Security enabled on all database tables.
- [x] **AWS Lambda Deployment** — Backend live on AWS via SST framework.
- [x] **Vercel Frontend** — React app fully deployed and connected to production backend.
