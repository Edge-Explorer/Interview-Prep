"""
====================================================================
 TEST RUNNER — Run ALL tests at once
====================================================================
 The master test runner for the entire InterviewAI backend.
 Runs every test file and prints a final summary report.

 HOW TO RUN:
   cd backend
   .\\venv\\Scripts\\python tests\\run_all_tests.py

 OPTIONS:
   --no-api    Skip API tests (use if backend is not running)
   --fast      Skip slow tests (agent, GPU)

 EXIT CODES:
   0 = All tests passed ✅
   1 = One or more tests failed ❌
====================================================================
"""

import subprocess
import sys
import os
import time

# Fix Windows terminal encoding (cp1252 can't print emojis)
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ── Colors for output ─────────────────────────────────────────────
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON = sys.executable

# ── Test definitions ──────────────────────────────────────────────
# (name, file, requires_server, is_slow)
TESTS = [
    ("Round Config",        "tests/test_round_config.py",       False, False),
    ("Discovery Data",      "tests/test_discovery_data.py",     False, False),
    ("Fuzzy Matching",      "tests/test_fuzzy_matching.py",     False, False),
    ("Company Intel",       "tests/test_company_intel.py",      False, False),
    ("Memory Service",      "tests/test_memory_service.py",     False, False),
    ("API Endpoints",       "tests/test_api_endpoints.py",      True,  False),
    ("Intelligence Agent",  "tests/test_intelligence_agent.py", False, True),
]

def run_test(name, file_path, timeout=120):
    abs_path = os.path.join(BACKEND_DIR, file_path)
    if not os.path.exists(abs_path):
        return "SKIP", 0, f"File not found: {abs_path}"

    # Inherit environment and add fixes for Windows
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"   # Fix emoji/unicode on Windows cp1252
    env["PYTHONPATH"] = BACKEND_DIR      # Fix ModuleNotFoundError for 'services'

    start = time.time()
    try:
        result = subprocess.run(
            [PYTHON, abs_path],
            cwd=BACKEND_DIR,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            env=env
        )
        elapsed = time.time() - start
        if result.returncode == 0:
            return "PASS", elapsed, result.stdout
        else:
            return "FAIL", elapsed, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return "TIMEOUT", timeout, f"Test timed out after {timeout}s"
    except Exception as e:
        return "ERROR", 0, str(e)


def main():
    args = sys.argv[1:]
    skip_api = "--no-api" in args
    fast_mode = "--fast" in args

    print(f"\n{BOLD}{CYAN}{'='*65}")
    print("  INTERVIEW AI — MASTER TEST RUNNER")
    print(f"{'='*65}{RESET}")
    print(f"  Backend dir: {BACKEND_DIR}")
    if skip_api:
        print(f"  {YELLOW}⚠️  Skipping API tests (--no-api){RESET}")
    if fast_mode:
        print(f"  {YELLOW}⚡ Fast mode — skipping slow tests{RESET}")
    print()

    results = []

    for name, file_path, requires_server, is_slow in TESTS:
        if requires_server and skip_api:
            print(f"  {YELLOW}⏩ SKIP{RESET} {name} (requires server)")
            results.append((name, "SKIP", 0, ""))
            continue
        if is_slow and fast_mode:
            print(f"  {YELLOW}⏩ SKIP{RESET} {name} (slow test)")
            results.append((name, "SKIP", 0, ""))
            continue

        print(f"  🔄 Running: {BOLD}{name}{RESET}...")
        status, elapsed, output = run_test(name, file_path)

        if status == "PASS":
            print(f"  {GREEN}✅ PASS{RESET} {name} ({elapsed:.1f}s)\n")
        elif status == "SKIP":
            print(f"  {YELLOW}⏩ SKIP{RESET} {name}\n")
        elif status == "TIMEOUT":
            print(f"  {RED}⏱️  TIMEOUT{RESET} {name} (>{elapsed:.0f}s)\n")
            # Print last few lines of output for debug
            lines = output.strip().split('\n')
            for line in lines[-5:]:
                print(f"      {line}")
            print()
        else:
            print(f"  {RED}❌ FAIL{RESET} {name} ({elapsed:.1f}s)")
            # Print last 10 lines of output
            lines = output.strip().split('\n')
            for line in lines[-10:]:
                print(f"      {line}")
            print()

        results.append((name, status, elapsed, output))

    # ── Final Summary ─────────────────────────────────────────────
    passed = sum(1 for _, s, _, _ in results if s == "PASS")
    failed = sum(1 for _, s, _, _ in results if s == "FAIL")
    skipped = sum(1 for _, s, _, _ in results if s == "SKIP")
    timed_out = sum(1 for _, s, _, _ in results if s == "TIMEOUT")

    print(f"\n{BOLD}{CYAN}{'='*65}")
    print("  FINAL REPORT")
    print(f"{'='*65}{RESET}")
    for name, status, elapsed, _ in results:
        if status == "PASS":
            icon, col = "✅", GREEN
        elif status == "FAIL":
            icon, col = "❌", RED
        elif status == "TIMEOUT":
            icon, col = "⏱️ ", YELLOW
        else:
            icon, col = "⏩", YELLOW
        print(f"  {col}{icon} {name}{RESET}")

    print(f"\n  Passed:   {GREEN}{passed}{RESET}")
    print(f"  Failed:   {RED}{failed}{RESET}")
    print(f"  Skipped:  {YELLOW}{skipped}{RESET}")
    print(f"  Timeout:  {YELLOW}{timed_out}{RESET}")

    total_run = passed + failed + timed_out
    if total_run:
        rate = passed / total_run * 100
        print(f"\n  {BOLD}Overall Success Rate: {rate:.0f}%{RESET}")

    if failed == 0 and timed_out == 0:
        print(f"\n  {GREEN}{BOLD}🎉 ALL TESTS PASSED! Safe to push to GitHub.{RESET}\n")
    else:
        print(f"\n  {RED}{BOLD}⛔ FAILURES DETECTED. DO NOT MERGE until fixed.{RESET}\n")

    return 0 if (failed == 0 and timed_out == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
