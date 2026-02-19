"""
Simple script to add a new company to the database
Just fill in the details below and run: python add_company.py
"""

import json
import os

# ============================================
# EDIT THIS SECTION TO ADD A NEW COMPANY
# ============================================

NEW_COMPANY = {
    "name": "Tesla",  # Company name
    "industry": "Technology/Automotive",  # Industry
    "size": "Large (>10000)",  # Company size
    "interview_style": "innovation-focused",  # Interview style
    "difficulty_level": "Very High",  # Difficulty: Medium, High, Very High
    "cultural_values": [
        "Move fast",
        "Think from first principles",
        "Question everything",
        "Work hard",
        "Make the impossible possible"
    ],
    "interview_rounds": {
        "Technical": {
            "focus": "First principles thinking, innovation, problem-solving",
            "common_topics": ["Physics problems", "Engineering challenges", "Optimization", "Real-world constraints"],
            "style": "Unconventional, focus on reasoning from first principles",
            "tips": "Show how you think, not just what you know. Question assumptions."
        },
        "Behavioral": {
            "focus": "Work ethic, passion, resilience",
            "common_questions": [
                "Tell me about the hardest problem you've solved",
                "How do you handle impossible deadlines?",
                "Why Tesla?"
            ],
            "style": "Direct, focus on real achievements and work ethic"
        },
        "System Design": {
            "focus": "Real-world engineering, physics constraints, innovation",
            "common_topics": ["Design battery management system", "Design autonomous driving", "Design charging network"],
            "style": "Focus on physics and real-world constraints"
        }
    },
    "red_flags": [
        "Not showing passion",
        "Giving up easily",
        "Not thinking from first principles",
        "Lack of work ethic"
    ],
    "average_process_duration": "4-8 weeks",
    "interview_count": "4-6 rounds"
}

# ============================================
# NO NEED TO EDIT BELOW THIS LINE
# ============================================

def add_company_to_database(company_data):
    """Add a new company to the database"""
    
    # Load existing data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, '..', 'data', 'company_profiles.json')
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Check if company already exists
    company_name = company_data['name']
    if company_name in data['companies']:
        print(f"⚠️  Company '{company_name}' already exists in database!")
        overwrite = input("Do you want to overwrite it? (yes/no): ").lower()
        if overwrite != 'yes':
            print("❌ Cancelled. No changes made.")
            return
    
    # Add the company
    data['companies'][company_name] = company_data
    data['meta']['total_companies'] = len(data['companies'])
    
    # Save updated data
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"\n✅ Successfully added '{company_name}' to the database!")
    print(f"📊 Total companies now: {data['meta']['total_companies']}")
    print(f"\n💡 Test it by running: python test_company_intel.py")

if __name__ == "__main__":
    print("="*60)
    print("ADDING NEW COMPANY TO DATABASE")
    print("="*60)
    print(f"\nCompany to add: {NEW_COMPANY['name']}")
    print(f"Industry: {NEW_COMPANY['industry']}")
    print(f"Difficulty: {NEW_COMPANY['difficulty_level']}")
    print("\nProceed? (Press Ctrl+C to cancel)")
    input("Press Enter to continue...")
    
    add_company_to_database(NEW_COMPANY)
