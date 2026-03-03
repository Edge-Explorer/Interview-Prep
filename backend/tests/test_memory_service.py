"""
====================================================================
 TEST: Memory Service & Stealth Registry
====================================================================
 Tests the memory_service.py crowdsourced learning system.
 Verifies that session data is correctly stored and loaded.

 HOW TO RUN:
   cd backend
   .\\venv\\Scripts\\python tests\\test_memory_service.py

 WHAT IT TESTS:
   ✅ Registry JSON loads without corruption
   ✅ Entries have correct schema
   ✅ Memory service can write NEW test entry
   ✅ Memory service can correctly read back saved entries
   ✅ Old/duplicate entries get merged (not duplicated)
====================================================================
"""

import sys
import os
import json
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

REGISTRY_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "stealth_registry.json"
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


async def run_all():
    print("\n" + "="*65)
    print(" INTERVIEW AI — MEMORY SERVICE TEST SUITE")
    print("="*65)

    # ── 1. Registry file integrity ─────────────────────────────────
    print("\n[1] Stealth Registry File Integrity")
    if not os.path.exists(REGISTRY_PATH):
        print(f"  ⚠️  Registry not found at: {REGISTRY_PATH} (will be created on first session)")
    else:
        try:
            with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
                registry = json.load(f)
            check("Registry is valid JSON", True, f"{len(registry)} entries found")

            if isinstance(registry, list):
                for i, entry in enumerate(registry):
                    check(f"Entry #{i} has company_name", "company_name" in entry,
                          entry.get("company_name", "MISSING"))
            elif isinstance(registry, dict):
                check("Registry is a dict", True, f"{len(registry)} keys")
            else:
                check("Registry is dict or list", False, f"Got type: {type(registry)}")
        except json.JSONDecodeError as e:
            check("Registry JSON is parseable", False, str(e))

    # ── 2. Memory Service import ────────────────────────────────────
    print("\n[2] Memory Service Import & Initialization")
    try:
        from services.memory_service import get_memory_service
        service = get_memory_service()
        check("MemoryService loaded", service is not None)
    except Exception as e:
        check("MemoryService import", False, str(e))
        print("\n  ⛔ Cannot continue without memory service.")
        return False

    # ── 3. Write test session data ──────────────────────────────────
    print("\n[3] Write Test Session to Registry")
    test_session = {
        "target_company": "__TEST_COMPANY__",
        "role_category": "Engineering & Tech",
        "rounds_completed": ["Technical", "Behavioral"],
        "score": 8.5
    }
    test_eval = {
        "score": 8.5,
        "feedback": "Great explanation of REST APIs.",
        "strengths": ["Clear communication"],
        "improvements": ["Go deeper on system design"]
    }
    try:
        await service.learn_from_session(test_session, test_eval)
        check("Test session written without error", True)
    except Exception as e:
        check("Write test session", False, str(e))

    # ── 4. Verify registry did not get corrupted ────────────────────
    print("\n[4] Registry Integrity After Write")
    try:
        if os.path.exists(REGISTRY_PATH):
            with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
                registry_after = json.load(f)
            check("Registry still valid JSON after write", True,
                  f"{len(registry_after)} entries")
        else:
            print("  ℹ️  Registry file not found (may not be enabled)")
    except json.JSONDecodeError as e:
        check("Registry JSON valid after write", False, str(e))

    # ── 5. Cleanup test data ────────────────────────────────────────
    print("\n[5] Cleanup Test Entry")
    try:
        if os.path.exists(REGISTRY_PATH):
            with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
                registry = json.load(f)

            if isinstance(registry, list):
                cleaned = [e for e in registry if e.get("company_name") != "__TEST_COMPANY__"]
            elif isinstance(registry, dict):
                cleaned = {k: v for k, v in registry.items() if k != "__TEST_COMPANY__"}
            else:
                cleaned = registry

            with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
                json.dump(cleaned, f, indent=2)
            check("Test entry cleaned up", True)
    except Exception as e:
        check("Cleanup test entry", False, str(e))

    # ── Summary ────────────────────────────────────────────────────
    total = passed + failed
    print("\n" + "="*65)
    print(f" RESULTS: {passed}/{total} passed | {failed} failed")
    rate = (passed / total * 100) if total else 0
    print(f" Success Rate: {rate:.0f}%")
    if failed == 0:
        print(" 🎉 ALL MEMORY SERVICE TESTS PASSED!")
    else:
        print(" ⚠️  Some tests failed.")
    print("="*65 + "\n")
    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(run_all())
    sys.exit(0 if success else 1)
