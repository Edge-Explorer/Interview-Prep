# Agentic Discoveries Database
This directory stores company intelligence profiles discovered dynamically by the **Multi-Agent Research Team**.

### How it works:
1. **Gatekeeper Agent**: Checks if the company is in the primary `company_profiles.json`.
2. **Researcher Agent**: Uses DuckDuckGo with **Temporal Dual-Search** for 2026 freshness.
3. **Auditor Agent (The Bouncer)**: Filters out SEO junk (Vastu/NCERT), verifies company identity against User JD, and generates an `audit_log`.
4. **Architect Agent (Llama-3)**: Processes only the **Audited Data** into a structured profile.
5. **Critic Agent (Gemini)**: Final quality assurance check.

### The Three-Path Discovery Flow:
1. **Public Firms (Web-Based)**: Audited research from professional domains.
2. **Identity-Collision Firms**: If the Auditor rejects all data (e.g., name collision with a non-tech entity), the system triggers **Synthetic Intelligence**.
3. **Stealth Startups (JD-Based)**: AI reverse-engineers company DNA if web results are zero.

### Developer Transparency:
Entries in `discoveries.json` include an `audit_log` with **ACCEPTED/REJECTED** statuses for all links. This log is for developer verification and is excluded from the end-user API.

5. **Persistence**: Once approved, the profile is saved here in `discoveries.json` so the system never has to research it twice.

### Author:
**Karan Shelar** - Architect of the Infinite Intelligence Loop.
