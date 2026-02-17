import asyncio
import os
from dotenv import load_dotenv
from services.intelligence_service import get_intelligence_service

load_dotenv()

async def test_agent():
    print("START: Starting Intelligence Service...")
    service = get_intelligence_service()
    
    # Test case 1: Known company (should be instant)
    print("\n--- Test 1: Known Company (Google) ---")
    google_intel = await service.get_intelligence("Google")
    print(f"DONE: Result: {google_intel.get('name')} - {google_intel.get('industry')}")
    
    # Test case 2: Unknown company (should trigger agent)
    company_name = "Antigravity Coding" 
    print(f"\n--- Test 2: Unknown Company ({company_name}) ---")
    new_intel = await service.get_intelligence(company_name)
    print(f"DONE: Final Agentic Result: {new_intel}")
    
    if "error" not in new_intel:
        print(f"SUCCESS: Successfully discovered intelligence for {company_name}")
    else:
        print(f"ERROR: Failed to discover {company_name}: {new_intel.get('error')}")

if __name__ == "__main__":
    import traceback
    try:
        asyncio.run(test_agent())
    except Exception:
        print("\nFATAL ERROR:")
        traceback.print_exc()
