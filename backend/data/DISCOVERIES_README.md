# Agentic Discoveries Database
This directory stores company intelligence profiles discovered dynamically by the **Multi-Agent Research Team**.

### How it works:
1. **Gatekeeper Agent**: Checks if the company is in the primary `company_profiles.json`.
2. **Router Agent**: Analyzes the company name for ambiguity and geographic location (Geographic Guarding).
3. **Researcher Agent**: Uses DuckDuckGo with **Evergreen Perpetual Freshness** (Auto-calculating Current Year).
4. **Auditor Agent (The Bouncer)**: Filters out SEO junk, verifies identity, and applies **Dynamic Domain Guarding** (prevents role forcing).
5. **Architect Agent (Llama-3)**: Processes Audited Data into a structured profile.
6. **Critic Agent (Gemini)**: Final quality assurance check.

### 📊 Confidence Score Matrix:
| Score | Status | Description |
| :--- | :--- | :--- |
| **0-20** | **Synthetic** | No web data; AI uses industry benchmarks. |
| **85** | **Verified** | Verified research data found and audited. |
| **100+** | **Elite** | High certainty; Matched Location, Industry, and direct interview data. |

### The Three-Path Discovery Flow:
1. **Public Firms (Web-Based)**: Audited research from professional domains.
2. **Identity-Collision Firms**: If the Auditor rejects all data, triggers **Synthetic Intelligence**.
3. **Stealth Startups (JD-Based)**: AI reverse-engineers DNA from the Job Description.

### Developer Transparency:
Entries in `discoveries.json` include an `audit_log` with **ACCEPTED/REJECTED** statuses for all links. This log is for developer verification and is excluded from the end-user API.

5. **Persistence**: Once approved, the profile is saved here in `discoveries.json` so the system never has to research it twice.

### Author:
**Karan Shelar** - Architect of the Infinite Intelligence Loop.
