# Agentic Discoveries Database
This directory stores company intelligence profiles discovered dynamically by the **Multi-Agent Research Team**.

### How it works:
1. **Gatekeeper Agent**: Checks if the company is in the primary `company_profiles.json`.
2. **Researcher Agent**: If not found, uses DuckDuckGo to gather live facts, news, and interview leaks.
3. **Architect Agent (Llama-3)**: Processes the messy research data into a structured interview profile.
4. **Critic Agent (Gemini)**: Validates the profile against schema requirements and industry reality.

### The Two-Path Discovery Flow:
1. **Public Firms (Web-Based)**: Researcher gathers news, articles, and reviews from the web.
2. **Stealth Startups (JD-Based)**: If web results are zero, the agents **reverse-engineer** the company DNA from the user's provided Job Description.

5. **Persistence**: Once approved, the profile is saved here in `discoveries.json` so the system never has to research it twice.

### Author:
**Karan Shelar** - Architect of the Infinite Intelligence Loop.
