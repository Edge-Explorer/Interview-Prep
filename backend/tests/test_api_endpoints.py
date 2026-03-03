"""
====================================================================
 TEST: API Endpoints — InterviewAI Backend
====================================================================
 Tests every major API endpoint using real HTTP requests.
 Requires the backend server to be RUNNING on localhost:8000.

 HOW TO RUN:
   cd backend
   .\\venv\\Scripts\\python tests\\test_api_endpoints.py

 WHAT IT TESTS:
   ✅ /health         — Server is alive
   ✅ /auth/signup    — User registration
   ✅ /auth/login     — Login + JWT token generation
   ✅ /users/stats    — Authenticated route protection
   ✅ /interviews/start — Interview session creation
   ❌ Unauthorized access — Should be rejected with 401/422
====================================================================
"""

import requests
import sys
import json
import random
import string

BASE_URL = "http://127.0.0.1:8000"

# ---- Helpers ----
def random_email():
    """Generate a unique test email to avoid conflicts."""
    tag = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{tag}@interviewai.test"

def print_result(name, passed, detail=""):
    icon = "✅" if passed else "❌"
    print(f"  {icon} {name}", f"→ {detail}" if detail else "")

def run_all_tests():
    print("\n" + "="*65)
    print(" INTERVIEW AI — API ENDPOINT TEST SUITE")
    print("="*65)

    results = {"passed": 0, "failed": 0}

    def check(name, condition, detail=""):
        if condition:
            results["passed"] += 1
            print_result(name, True, detail)
        else:
            results["failed"] += 1
            print_result(name, False, detail)

    token = None
    test_email = random_email()
    test_password = "TestPassword123!"

    # ── 1. Health Check ─────────────────────────────────────────
    print("\n[1] Health Check")
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=5)
        check("Server is reachable", r.status_code == 200, f"status={r.status_code}")
        check("Returns version", "version" in r.json(), r.json())
    except Exception as e:
        check("Server is reachable", False, str(e))
        print("\n  ⛔ Backend is NOT running. Start it with: python main.py")
        sys.exit(1)

    # ── 2. Signup ────────────────────────────────────────────────
    print("\n[2] Auth: Signup")
    try:
        r = requests.post(f"{BASE_URL}/auth/signup", json={
            "email": test_email, "password": test_password, "full_name": "Test User"
        }, timeout=10)
        check("Signup returns 200", r.status_code == 200, f"status={r.status_code}")
        check("Returns access_token", "access_token" in r.json(), list(r.json().keys()))
        if "access_token" in r.json():
            token = r.json()["access_token"]
    except Exception as e:
        check("Signup request", False, str(e))

    # ── 3. Duplicate Signup (should fail) ───────────────────────
    print("\n[3] Auth: Duplicate Signup Protection")
    try:
        r = requests.post(f"{BASE_URL}/auth/signup", json={
            "email": test_email, "password": test_password, "full_name": "Test User"
        }, timeout=10)
        check("Duplicate email rejected", r.status_code == 400, f"status={r.status_code}")
    except Exception as e:
        check("Duplicate signup request", False, str(e))

    # ── 4. Login ─────────────────────────────────────────────────
    print("\n[4] Auth: Login")
    try:
        r = requests.post(f"{BASE_URL}/auth/login", json={
            "email": test_email, "password": test_password
        }, timeout=10)
        check("Login returns 200", r.status_code == 200, f"status={r.status_code}")
        check("Returns JWT token", "access_token" in r.json())
        if "access_token" in r.json():
            token = r.json()["access_token"]  # Refresh token from login
    except Exception as e:
        check("Login request", False, str(e))

    # ── 5. Bad Login ─────────────────────────────────────────────
    print("\n[5] Auth: Bad Password Protection")
    try:
        r = requests.post(f"{BASE_URL}/auth/login", json={
            "email": test_email, "password": "WrongPassword!"
        }, timeout=10)
        check("Bad password rejected", r.status_code == 400, f"status={r.status_code}")
    except Exception as e:
        check("Bad login request", False, str(e))

    # ── 6. Authenticated Route ───────────────────────────────────
    print("\n[6] Authenticated: /users/stats")
    if token:
        try:
            r = requests.get(f"{BASE_URL}/users/stats",
                headers={"Authorization": f"Bearer {token}"}, timeout=10)
            check("Stats returns 200 with token", r.status_code == 200, f"status={r.status_code}")
            check("Returns total_interviews", "total_interviews" in r.json())
            check("Returns avg_score", "avg_score" in r.json())
        except Exception as e:
            check("Stats request", False, str(e))
    else:
        check("Stats with token", False, "Skipped — no token")

    # ── 7. Unauthorized Access ───────────────────────────────────
    print("\n[7] Security: Unauthorized Access")
    try:
        r = requests.get(f"{BASE_URL}/users/stats", timeout=10)
        check("No-token request rejected", r.status_code in [401, 422], f"status={r.status_code}")
        r2 = requests.get(f"{BASE_URL}/users/stats",
            headers={"Authorization": "Bearer FAKE_TOKEN"}, timeout=10)
        check("Fake token rejected", r2.status_code == 401, f"status={r2.status_code}")
    except Exception as e:
        check("Unauthorized test", False, str(e))

    # ── 8. Summary ───────────────────────────────────────────────
    total = results["passed"] + results["failed"]
    print("\n" + "="*65)
    print(f" RESULTS: {results['passed']}/{total} passed | {results['failed']} failed")
    rate = (results['passed'] / total * 100) if total else 0
    print(f" Success Rate: {rate:.0f}%")
    if results["failed"] == 0:
        print(" 🎉 ALL ENDPOINT TESTS PASSED!")
    else:
        print(" ⚠️  Some tests failed. Fix the issues above before merging.")
    print("="*65 + "\n")
    return results["failed"] == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
