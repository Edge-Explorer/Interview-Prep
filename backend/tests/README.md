# 🧪 InterviewAI — Test Suite

This directory contains the **core test suite** for the InterviewAI backend. Every contributor **MUST** run these tests before submitting a Pull Request. If any test fails, the code should **NOT** be merged.

---

## 📂 Test Files

| File | What It Tests | Needs Server? | Speed |
|---|---|---|---|
| `run_all_tests.py` | **Master runner — runs everything** | No | Fast |
| `test_round_config.py` | Domain-aware round sequences & pass scores | No | ⚡ Fast |
| `test_discovery_data.py` | `discoveries.json` integrity & schema guard | No | ⚡ Fast |
| `test_fuzzy_matching.py` | Company name typo/alias matching | No | ⚡ Fast |
| `test_company_intel.py` | Tier 1 curated company database lookups | No | ⚡ Fast |
| `test_memory_service.py` | Stealth registry write/read & cleanup | No | ⚡ Fast |
| `test_api_endpoints.py` | All REST API routes + auth security | **Yes** | 🐢 Medium |
| `test_intelligence_agent.py` | Full AI discovery agent pipeline | No | 🐢 Slow |
| `check_gpu.py` | CUDA GPU diagnostic for local Llama-3 | No | ⚡ Fast |

---

## 🚀 How to Run

> **Always run from the `backend/` directory with the venv activated.**

### ✅ Run ALL fast tests (recommended before any PR):
```powershell
cd backend
.\venv\Scripts\Activate
$env:PYTHONIOENCODING="utf-8"
.\venv\Scripts\python tests\run_all_tests.py --no-api --fast
```

### 🌐 Full run (with backend server running on port 8000):
```powershell
.\venv\Scripts\python tests\run_all_tests.py
```

### ⚡ Skip API tests only (server not running):
```powershell
.\venv\Scripts\python tests\run_all_tests.py --no-api
```

### 🔬 Run a single test file:
```powershell
.\venv\Scripts\python tests\test_round_config.py
.\venv\Scripts\python tests\test_discovery_data.py
.\venv\Scripts\python tests\test_fuzzy_matching.py
.\venv\Scripts\python tests\test_company_intel.py
.\venv\Scripts\python tests\test_memory_service.py
.\venv\Scripts\python tests\test_api_endpoints.py   # needs server
```

### 🧠 Test AI agent on a specific company:
```powershell
.\venv\Scripts\python tests\test_intelligence_agent.py "Zepto"
.\venv\Scripts\python tests\test_intelligence_agent.py "Morgan Stanley"
```

### 🖥️ Check GPU / CUDA status:
```powershell
.\venv\Scripts\python tests\check_gpu.py
```

---

## 📋 Contributor Rules

### ➕ Adding a new company to `discoveries.json`
This is **mandatory** before pushing:
```powershell
.\venv\Scripts\python tests\test_discovery_data.py
```
This catches:
- ❌ Duplicate company entries
- ❌ Missing required fields (`name`, `industry`, `interview_rounds`)
- ❌ Corrupted or unparseable JSON
- ⚠️ Placeholder values like `"TODO"` or `"N/A"`

### 🔧 Modifying `round_config.py`
```powershell
.\venv\Scripts\python tests\test_round_config.py
```
Ensures all domains have valid round sequences for all 3 difficulty levels.

### 🌐 Changing any API endpoint in `main.py`
```powershell
# Start server first: python main.py
.\venv\Scripts\python tests\test_api_endpoints.py
```

### 🧠 Touching `intelligence_service.py` or `memory_service.py`
```powershell
.\venv\Scripts\python tests\test_memory_service.py
.\venv\Scripts\python tests\test_intelligence_agent.py "Google"
```

---

## 🛡️ Merge Policy

1. Run `run_all_tests.py --no-api --fast`
2. If output shows **any** `❌ FAIL` — **DO NOT MERGE**
3. Fix all failures, re-run until you see:
   ```
   🎉 ALL TESTS PASSED! Safe to push to GitHub.
   ```
4. Only then submit your Pull Request

---

## ✅ Expected Output (clean run)

```
=================================================================
  INTERVIEW AI — MASTER TEST RUNNER
=================================================================

  ✅ PASS Round Config      (0.1s)
  ✅ PASS Discovery Data    (0.1s)
  ✅ PASS Fuzzy Matching    (0.1s)
  ✅ PASS Company Intel     (0.1s)
  ✅ PASS Memory Service    (0.2s)
  ⏩ SKIP API Endpoints     (requires server)
  ⏩ SKIP Intelligence Agent (slow test)

  Overall Success Rate: 100%
  🎉 ALL TESTS PASSED! Safe to push to GitHub.
```
