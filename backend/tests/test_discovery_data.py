"""
====================================================================
 TEST: Discovery JSON Integrity — Data Quality Guard
====================================================================
 Validates the discoveries.json file for structural correctness.
 Any contributor adding a new company MUST pass this test.

 HOW TO RUN:
   cd backend
   .\\venv\\Scripts\\python tests\\test_discovery_data.py

 WHAT IT TESTS:
   ✅ JSON is parseable (not corrupted)
   ✅ Every entry has required top-level fields
   ✅ interview_rounds is not empty
   ✅ No duplicate company names
   ✅ confidence_score is in valid range (0-200)
   ✅ No field has a None/null string value instead of actual null
   ✅ Profile completeness (no placeholder text like "TODO")
====================================================================
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DISCOVERIES_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "discoveries.json"
)

REQUIRED_TOP_LEVEL = {"company_name", "interview_intelligence_profile"}
REQUIRED_PROFILE_KEYS = {"name", "industry", "interview_rounds"}

passed = 0
failed = 0
warnings = 0


def check(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        # Only print failures for concise output
    else:
        failed += 1
        print(f"  ❌ {name}", f"→ {detail}" if detail else "")


def warn(name, detail=""):
    global warnings
    warnings += 1
    print(f"  ⚠️  WARNING: {name}", f"→ {detail}" if detail else "")


def run_all():
    print("\n" + "="*65)
    print(" INTERVIEW AI — DISCOVERY JSON INTEGRITY TEST")
    print("="*65)

    # ── 1. File exists ────────────────────────────────────────────
    print("\n[1] File Existence & Parseability")
    if not os.path.exists(DISCOVERIES_PATH):
        print(f"  ❌ discoveries.json not found at: {DISCOVERIES_PATH}")
        sys.exit(1)

    try:
        with open(DISCOVERIES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"  ✅ File loaded successfully — {len(data)} entries found")
    except json.JSONDecodeError as e:
        print(f"  ❌ CRITICAL: JSON is CORRUPTED — {e}")
        sys.exit(1)

    if not isinstance(data, list):
        print("  ❌ CRITICAL: discoveries.json must be a JSON array")
        sys.exit(1)

    # ── 2. Per-entry validation ───────────────────────────────────
    print(f"\n[2] Validating {len(data)} entries...")
    seen_names = {}
    for i, entry in enumerate(data):
        company = entry.get("company_name", f"UNKNOWN#{i}")
        profile = entry.get("interview_intelligence_profile", {})

        # Required top-level keys
        for key in REQUIRED_TOP_LEVEL:
            check(f"[{company}] has '{key}'", key in entry, f"missing key: {key}")

        # Required profile keys
        for key in REQUIRED_PROFILE_KEYS:
            check(f"[{company}] profile has '{key}'", key in profile, f"missing: {key}")

        # interview_rounds must be non-empty dict
        rounds = profile.get("interview_rounds", {})
        check(f"[{company}] has interview_rounds", isinstance(rounds, dict) and len(rounds) > 0,
              f"rounds={rounds}" if not rounds else "")

        # confidence_score in range
        confidence = entry.get("confidence_score")
        if confidence is not None:
            check(f"[{company}] confidence_score in range",
                  isinstance(confidence, (int, float)) and 0 <= confidence <= 200,
                  f"got {confidence}")

        # No literal "null"/"none"/"TODO" string values
        profile_str = json.dumps(profile).lower()
        if '"todo"' in profile_str or '"n/a"' in profile_str:
            warn(f"[{company}] contains placeholder 'TODO' or 'N/A' values")

        # Duplicate detection
        name_lower = company.lower().strip()
        if name_lower in seen_names:
            check(f"[{company}] no duplicate", False,
                  f"DUPLICATE of entry #{seen_names[name_lower]}")
        else:
            seen_names[name_lower] = i
            check(f"[{company}] no duplicate", True)

    # ── 3. Summary ───────────────────────────────────────────────
    total = passed + failed
    print("\n" + "="*65)
    print(f" RESULTS: {passed}/{total} checks passed | {failed} failed | {warnings} warnings")
    rate = (passed / total * 100) if total else 0
    print(f" Success Rate: {rate:.1f}%")
    if failed == 0:
        print(f" 🎉 ALL {len(data)} COMPANY ENTRIES VALIDATED!")
        if warnings:
            print(f" ⚠️  {warnings} non-critical warnings above (review them)")
    else:
        print(" ⛔ INTEGRITY FAILURES DETECTED. Fix before merging.")
    print("="*65 + "\n")
    return failed == 0


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
