"""
Test fuzzy company matching
"""

from services.company_intelligence import get_company_intelligence

def test_fuzzy_matching():
    """Test various company name variations"""
    
    service = get_company_intelligence()
    
    print("="*60)
    print("TESTING FUZZY COMPANY MATCHING")
    print("="*60)
    
    # Test cases: (input, expected_company)
    test_cases = [
        # Case variations
        ("google", "Google"),
        ("GOOGLE", "Google"),
        ("GoOgLe", "Google"),
        
        # Spacing variations
        ("open ai", "OpenAI"),
        ("openai", "OpenAI"),
        ("OPENAI", "OpenAI"),
        
        # Typos
        ("gogle", "Google"),  # Missing 'o'
        ("amazn", "Amazon"),  # Missing 'o'
        ("microsft", "Microsoft"),  # Missing 'o'
        ("opnai", "OpenAI"),  # Typo
        
        # Aliases
        ("fb", "Meta"),
        ("facebook", "Meta"),
        ("claude", "Anthropic"),
        ("stable diffusion", "Stability AI"),
        ("hf", "Hugging Face"),
        ("huggingface", "Hugging Face"),
        
        # Finance
        ("goldman", "Goldman Sachs"),
        ("jpmorgan", "JPMorgan Chase"),
        ("jp morgan", "JPMorgan Chase"),
        
        # Consulting
        ("mckinsey", "McKinsey & Company"),
        ("bcg", "Boston Consulting Group"),
        ("pwc", "PwC (PricewaterhouseCoopers)"),
        
        # Indian companies
        ("flipkrt", "Flipkart"),  # Typo
        ("razorpay", "Razorpay"),
        ("dream11", "Dream11"),
        
        # AI companies
        ("perplexity", "Perplexity AI"),
        ("character ai", "Character.AI"),
        ("characterai", "Character.AI"),
        ("midjourny", "Midjourney"),  # Typo
    ]
    
    passed = 0
    failed = 0
    
    for input_name, expected in test_cases:
        profile = service.get_company_profile(input_name)
        
        if profile:
            actual = profile['name']
            if actual == expected:
                print(f"✅ '{input_name}' → '{actual}'")
                passed += 1
            else:
                print(f"⚠️  '{input_name}' → '{actual}' (expected '{expected}')")
                failed += 1
        else:
            print(f"❌ '{input_name}' → NOT FOUND (expected '{expected}')")
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print(f"Success rate: {passed/len(test_cases)*100:.1f}%")
    print(f"{'='*60}")

if __name__ == "__main__":
    test_fuzzy_matching()
