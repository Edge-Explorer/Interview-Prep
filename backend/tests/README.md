# 🧪 InterviewAI — Test Suite

This directory contains the **full test suite** for the InterviewAI backend. Every contributor **MUST** run these tests before submitting a Pull Request. If any test fails, the code should **NOT** be merged.

---

## 📂 Test Files Overview

| File | What It Tests | Needs Server? | Speed |
|---|---|---|---|
| `run_all_tests.py` | **Master runner — runs everything** | No | Fast |
| `test_round_config.py` | Domain-aware round sequences | No | ⚡ Fast |
| `test_discovery_data.py` | `discoveries.json` data integrity | No | ⚡ Fast |
| `test_fuzzy_matching.py` | Company name typo/alias matching | No | ⚡ Fast |
| `test_company_intel.py` | Tier 1 curated company database | No | ⚡ Fast |
| `test_memory_service.py` | Stealth registry write/read | No | ⚡ Fast |
| `test_api_endpoints.py` | All REST API routes + auth | **Yes** | 🐢 Medium |
| `test_intelligence_agent.py` | Full AI discovery agent pipeline | No | 🐢 Slow (AI calls) |

---

## 🚀 How to Run Tests

> **Always run from the `backend/` directory.**

### ✅ Run ALL tests at once (recommended before any PR):
```powershell
cd backend
.\venv\Scripts\python tests\run_all_tests.py
```

### ⚡ Fast mode (skip slow AI tests):
```powershell
.\venv\Scripts\python tests\run_all_tests.py --fast
```

### 🌐 Skip API tests (if backend server is NOT running):
```powershell
.\venv\Scripts\python tests\run_all_tests.py --no-api
```

### 🔬 Run a single test:
```powershell
.\venv\Scripts\python tests\test_round_config.py
.\venv\Scripts\python tests\test_discovery_data.py
.\venv\Scripts\python tests\test_fuzzy_matching.py
.\venv\Scripts\python tests\test_api_endpoints.py
.\venv\Scripts\python tests\test_memory_service.py
```

### 🧠 Test the AI agent on a specific company:
```powershell
.\venv\Scripts\python tests\test_intelligence_agent.py "Zepto"
.\venv\Scripts\python tests\test_intelligence_agent.py "Morgan Stanley"
```

---

## 📋 Rules for Contributors

### Adding a New Company to `discoveries.json`
If you're adding a company, run this MANDATORY check:
```powershell
.\venv\Scripts\python tests\test_discovery_data.py
```
This will catch:
- ❌ Duplicate entries
- ❌ Missing required fields (`interview_rounds`, `name`, `industry`)
- ❌ Corrupted JSON
- ⚠️ Placeholder text like "TODO" or "N/A"

### Adding a New Round Domain to `round_config.py`
Run:
```powershell
.\venv\Scripts\python tests\test_round_config.py
```
This ensures your new domain has valid sequences for all 3 difficulty levels.

### Changing any API endpoint in `main.py`
Run:
```powershell
# Start your backend first: python main.py
.\venv\Scripts\python tests\test_api_endpoints.py
```

### Touching `memory_service.py` or `stealth_registry.json`
Run:
```powershell
.\venv\Scripts\python tests\test_memory_service.py
```

---

## 🛡️ What happens if a contributor submits bad code?

1. **Run `run_all_tests.py`** — if it shows ❌ failures, the PR is REJECTED.
2. The contributor must fix all failures and re-run the suite.
3. Only when you see `🎉 ALL TESTS PASSED! Safe to push to GitHub.` is the code mergeable.

---

## 🔧 GPU Diagnostic
If you suspect GPU issues with the local Llama-3 model:
```powershell
.\venv\Scripts\python tests\check_gpu.py
```
This shows your CUDA version, VRAM usage, and whether the model can be loaded.
