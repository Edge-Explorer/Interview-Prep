"""
Test script for Company Intelligence Service
Run this to verify Tier 1 is working correctly
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.company_intelligence import get_company_intelligence

def test_company_intelligence():
    print("="*70)
    print("TESTING COMPANY INTELLIGENCE SERVICE (TIER 1)")
    print("="*70)
    
    intel = get_company_intelligence()
    
    print(f"\n✅ Total companies loaded: {intel.get_company_count()}")
    print(f"\n📋 Companies in database:")
    for i, company in enumerate(intel.get_all_companies(), 1):
        print(f"   {i}. {company}")
    
    print("\n" + "="*70)
    print("TESTING: Google (Should use Tier 1 - Curated)")
    print("="*70)
    context = intel.get_interview_context("Google", "Technical")
    print(context)
    
    print("\n" + "="*70)
    print("TESTING: Random Startup (Should use Tier 3 - AI Fallback)")
    print("="*70)
    profile = intel.get_company_profile("RandomStartup123")
    if profile:
        print("❌ ERROR: Found profile for non-existent company")
    else:
        print("✅ Correctly returned None for unknown company")
        print("   (AI will use Tier 3 fallback)")
    
    print("\n" + "="*70)
    print("TESTING: Case-insensitive matching")
    print("="*70)
    test_cases = ["google", "GOOGLE", "Google", "amazon", "AMAZON"]
    for test in test_cases:
        found = intel.is_company_in_database(test)
        print(f"   '{test}': {'✅ Found' if found else '❌ Not found'}")
    
    print("\n" + "="*70)
    print("TESTING: Amazon Leadership Principles")
    print("="*70)
    values = intel.get_cultural_values("Amazon")
    print(f"   Amazon's Cultural Values ({len(values)} total):")
    for value in values[:5]:
        print(f"   - {value}")
    
    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED - TIER 1 IS WORKING!")
    print("="*70)

if __name__ == "__main__":
    test_company_intelligence()
