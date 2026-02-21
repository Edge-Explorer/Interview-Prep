import asyncio
import os
import os
import sys
# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
    
    # Use CLI argument if provided, else default to Antigravity
    import sys
    company_name = sys.argv[1] if len(sys.argv) > 1 else "Antigravity Coding"
    
    # Optional: Pass a JD to test "Stealth Mode"
    jd = "Search for a tech role at an AI startup" 
    
    print(f"\n--- Test: Autonomous Discovery ({company_name}) ---")
    new_intel = await service.get_intelligence(company_name, jd)
    print(f"DONE: Final Agentic Result: {new_intel}")
    
    if "sources" in new_intel and new_intel["sources"]:
        print("\nSOURCES FOUND:")
        for i, source in enumerate(new_intel["sources"], 1):
            print(f"   {i}. {source['title']} -> {source['url']}")
    
    # 'error' key is always present in result — None means success, a string means failure
    if not new_intel.get('error'):
        is_synthetic = new_intel.get('is_synthetic', False)
        confidence  = new_intel.get('confidence_score', 'N/A')
        industry    = new_intel.get('industry', 'Unknown')
        print(f"SUCCESS: Discovered '{company_name}'")
        print(f"   Industry    : {industry}")
        print(f"   Confidence  : {confidence}")
        print(f"   Synthetic   : {is_synthetic}")
        rounds = new_intel.get('interview_rounds', {})
        if rounds:
            print(f"   Rounds      : {', '.join(rounds.keys())}")
    else:
        print(f"ERROR: Failed to discover {company_name}: {new_intel.get('error')}")

if __name__ == "__main__":
    import traceback
    try:
        asyncio.run(test_agent())
    except Exception as e:
        print(f"\nFATAL ERROR: {str(e)}")
        traceback.print_exc()
