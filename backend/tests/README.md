# 🧪 Test Suite - Verification & Validation

This directory contains the automated test suite for ensuring the backend services and AI agents are functioning correctly.

## 📂 Key Tests

1. **`test_intelligence_agent.py`**:
    - The main test for the LangGraph-based Intelligence Service.
    - Tests the full Researcher -> Architect -> Critic loop.
    - Supports CLI arguments for testing specific companies.

2. **`test_company_intel.py`**:
    - Verifies the Tier 1 logic (Curated Database lookup).
    - Checks for correct context generation and profile loading.

3. **`test_fuzzy_matching.py`**:
    - Benchmarks the `rapidfuzz` implementation.
    - Ensures that variations like "Google Inc" vs "Google" are correctly mapped.

4. **`check_gpu.py`**:
    - A utility to verify if PyTorch can detect local CUDA devices for Llama-3 acceleration.

## 🚀 Running Tests

Always run tests from the `backend` root to ensure correct path discovery:
```bash
.\venv\Scripts\python tests\test_intelligence_agent.py "Google"
```
