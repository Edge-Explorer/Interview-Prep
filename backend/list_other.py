import json

def list_uncategorized():
    with open('data/company_profiles.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    mapping = {
        "Engineering & Tech": ["Technology", "Software", "AI", "SaaS", "Gaming", "Cybersecurity", "Cloud", "Social Media", "Hardware", "Semiconductors", "Networking", "Computing", "Observability", "Integration", "AdTech"],
        "Healthcare & Medical": ["Healthcare", "Medical", "Biotech", "E-Pharmacy", "Health IT", "EHR", "Diagnostics", "Pharma", "Fitness"],
        "Business & Management": ["Consulting", "Staffing", "HR", "Business", "Enterprise SaaS", "Contracts"],
        "Finance & Accounting": ["Fintech", "Banking", "Payments", "Trading", "Finance", "Investment", "Insurance"],
        "Creative & Design": ["Creative", "Media", "Entertainment", "Music", "Video", "Streaming", "Art", "Design"],
        "Sales & Marketing": ["Marketing", "E-commerce"],
        "Education & Training": ["EdTech", "Education"],
        "Legal": ["Legal"],
        "Construction & Trades": ["Logistics", "Real Estate", "Automotive", "Autonomous Driving", "Aerospace", "PropTech", "Supply Chain"],
        "Social Services": ["Non-profit", "Community"],
        "Science & Research": ["Research", "Science", "Space"]
    }
    
    for name, info in data['companies'].items():
        industry = info.get('industry', '').lower()
        found = False
        for domain, keywords in mapping.items():
            if any(kw.lower() in industry for kw in keywords):
                found = True
                break
        if not found:
            print(f"{name}: {info.get('industry')}")

if __name__ == "__main__":
    list_uncategorized()
