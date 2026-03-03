"""
====================================================================
 TEST: Round Configuration — Domain-Aware Round System
====================================================================
 Tests the round_config.py module in isolation (no server needed).

 HOW TO RUN:
   cd backend
   .\\venv\\Scripts\\python tests\\test_round_config.py

 WHAT IT TESTS:
   ✅ Correct round sequences per domain and difficulty
   ✅ First round returned correctly
   ✅ Next round logic (no out-of-bounds errors)
   ✅ Pass/Fail score thresholds
   ✅ Unknown domain falls back to 'default'
   ✅ Difficulty clamping (no crash on level 0 or 99)
====================================================================
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.round_config import (
    get_round_sequence,
    get_first_round,
    get_next_round,
    get_round_config,
    should_proceed_to_next_round,
    DOMAIN_ROUND_SEQUENCES,
    ROUND_DEFINITIONS
)

passed = 0
failed = 0

def check(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  ✅ {name}", f"→ {detail}" if detail else "")
    else:
        failed += 1
        print(f"  ❌ {name}", f"→ {detail}" if detail else "")


def run_all():
    print("\n" + "="*65)
    print(" INTERVIEW AI — ROUND CONFIG TEST SUITE")
    print("="*65)

    # ── 1. All domains are defined ────────────────────────────────
    print("\n[1] Domain Coverage")
    for domain in DOMAIN_ROUND_SEQUENCES:
        if domain == "default":
            continue
        for level in [1, 2, 3]:
            seq = get_round_sequence(domain, level)
            check(f"{domain} Level {level}", len(seq) > 0, seq)

    # ── 2. First Round Logic ──────────────────────────────────────
    print("\n[2] First Round Returned Correctly")
    cases = [
        ("Engineering & Tech", 1, "Technical"),
        ("Finance & Accounting", 2, "Domain Knowledge"),
        ("Creative & Design", 1, "Portfolio Review"),
        ("Healthcare & Medical", 3, "Domain Knowledge"),
        ("Sales & Marketing", 2, "Domain Knowledge"),
    ]
    for domain, level, expected in cases:
        result = get_first_round(domain, level)
        check(f"{domain} L{level} first round", result == expected, f"got '{result}', expected '{expected}'")

    # ── 3. Next Round ─────────────────────────────────────────────
    print("\n[3] Next Round Logic")
    # Engineering Senior: Technical → System Design → Behavioral → Managerial → Final → None
    check("Technical → System Design", get_next_round("Technical", "Engineering & Tech", 3) == "System Design")
    check("Behavioral → Managerial (L3)", get_next_round("Behavioral", "Engineering & Tech", 3) == "Managerial")
    check("Final → None (interview ends)", get_next_round("Final", "Engineering & Tech", 3) is None)
    check("Last round L1 → None", get_next_round("Behavioral", "Engineering & Tech", 1) is None)

    # ── 4. Pass/Fail Thresholds ───────────────────────────────────
    print("\n[4] Pass/Fail Score Thresholds")
    for round_name, config in ROUND_DEFINITIONS.items():
        pass_score = config["pass_score"]
        check(f"{round_name}: score {pass_score} passes", should_proceed_to_next_round(pass_score, round_name))
        check(f"{round_name}: score {pass_score - 0.1:.1f} fails", not should_proceed_to_next_round(pass_score - 0.1, round_name))

    # ── 5. Unknown Domain Fallback ────────────────────────────────
    print("\n[5] Unknown Domain Fallback")
    seq = get_round_sequence("Underwater Basket Weaving", 2)
    check("Unknown domain falls back", len(seq) > 0, seq)

    # ── 6. Difficulty Clamping (edge cases) ───────────────────────
    print("\n[6] Difficulty Clamping")
    seq_0 = get_round_sequence("Engineering & Tech", 0)
    seq_99 = get_round_sequence("Engineering & Tech", 99)
    check("Level 0 clamped to Level 1", seq_0 is not None and len(seq_0) > 0, seq_0)
    check("Level 99 clamped to Level 3", seq_99 is not None and len(seq_99) > 0, seq_99)

    # ── 7. All round definitions have required keys ───────────────
    print("\n[7] Round Definition Schema Completeness")
    required_keys = {"description", "min_questions", "max_questions", "pass_score"}
    for round_name, config in ROUND_DEFINITIONS.items():
        missing = required_keys - set(config.keys())
        check(f"{round_name} has all required keys", len(missing) == 0, f"missing: {missing}" if missing else "")

    # ── Summary ───────────────────────────────────────────────────
    total = passed + failed
    print("\n" + "="*65)
    print(f" RESULTS: {passed}/{total} passed | {failed} failed")
    rate = (passed / total * 100) if total else 0
    print(f" Success Rate: {rate:.0f}%")
    if failed == 0:
        print(" 🎉 ALL ROUND CONFIG TESTS PASSED!")
    else:
        print(" ⚠️  Some tests failed. Fix before merging.")
    print("="*65 + "\n")
    return failed == 0

if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
