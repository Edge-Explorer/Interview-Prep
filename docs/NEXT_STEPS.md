# 🚀 The Journey Ahead: Next Steps

This document outlines the strategic roadmap and upcoming technical features for **InterviewAI**.

---

## 🎯 Short-Term Goals (Next 2 Weeks)

### 1. 🌐 Public Deployment
- [ ] **Backend**: Deploy FastAPI to Render or AWS Lambda.
- [ ] **Frontend**: Deploy React app to Vercel/Netlify.
- [ ] **Environment**: Centralize all `VITE_API_URL` variables for production.

### 2. ⚡ UI/UX "Agentic" Feedback
- [ ] Add a "Researcher at Work" loading terminal in the UI.
- [ ] Show the user when the AI is in "Stealth Mode" vs "Public Research" mode.
- [ ] Polish the `discoveries.json` visual rendering in the dashboard.

- [ ] Implement a final "Hiring Decision" report after all 5 rounds.
- [ ] Implement iterative difficulty scaling (Round 2 is harder if Round 1 was 'Elite').

### 4. 🧠 Intelligence Refinement (Phase 2.5)
- [ ] **Cross-Continental Localization**: Enhance the Router to detect if a company has different processes (e.g., Google US vs Google India).
- [ ] **Discovery Dashboard**: Create a UI screen to browse the global `discoveries.json` database.
- [ ] **Real-time Search Streaming**: Push live research logs (ACCEPTED/REJECTED links) directly to the user's dashboard for transparency.
- [ ] **Automatic Memory Pruning**: Build a script to periodically "refresh" discoveries that are older than 6 months.

---

## 🏔️ Long-Term Vision (Future Roadmap)

### 📊 AI-Generated Learning Roadmaps
- Build the logic to transform interview feedback into a personalized 7-day study plan stored in the database.

### 🎥 Video/Voice Integration
- Implement real-time WebRTC logic to analyze body language and tone during the session.

### 🏆 Community & Scores
- Create a global leaderboard for "Google-Level" readiness scores.
- Allow users to share their "Interview Intelligence Reports" on LinkedIn.

---

## 💡 Tech Debt & Maintenance
- [ ] Refine the "Critic" agent prompts to be even more strict.
- [ ] Expand the Curated Database from 383 companies to 500+.
- [ ] Implement robust error handling for DuckDuckGo rate limits.
