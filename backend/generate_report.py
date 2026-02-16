import json
from collections import Counter

def generate_domain_report():
    with open('data/company_profiles.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    companies = data['companies']
    
    # Mapping industries to the 12 main frontend categories
    mapping = {
        "Engineering & Tech": ["Technology", "Software", "AI", "SaaS", "Gaming", "Cybersecurity", "Cloud", "Social Media", "Hardware", "Semiconductors", "Networking", "Computing", "Observability", "Integration", "AdTech", "E-commerce"],
        "Healthcare & Medical": ["Healthcare", "Medical", "Biotech", "E-Pharmacy", "Health IT", "EHR", "Diagnostics", "Pharma", "Fitness"],
        "Business & Management": ["Consulting", "Staffing", "HR", "Business", "Enterprise SaaS", "Contracts", "CRM"],
        "Finance & Accounting": ["Fintech", "Banking", "Payments", "Trading", "Finance", "Investment", "Insurance"],
        "Creative & Design": ["Creative", "Media", "Entertainment", "Music", "Video", "Streaming", "Art", "Design"],
        "Sales & Marketing": ["Marketing"],
        "Education & Training": ["EdTech", "Education"],
        "Legal": ["Legal", "Law"],
        "Construction & Trades": ["Logistics", "Real Estate", "Automotive", "Autonomous Driving", "Aerospace", "PropTech", "Supply Chain", "Construction", "Engineering"],
        "Hospitality & Tourism": ["Travel", "Hospitality", "Hotel", "Tourism", "Booking", "Marketplace", "Delivery", "Food"],
        "Social Services": ["Non-profit", "Community", "Philanthropy", "Social Services"],
        "Science & Research": ["Research", "Science", "Space"]
    }
    
    domain_counts = Counter()
    
    for name, info in companies.items():
        industry = info.get('industry', 'Unknown').lower()
        found = False
        for domain, keywords in mapping.items():
            if any(kw.lower() in industry for kw in keywords):
                domain_counts[domain] += 1
                found = True
                break
        if not found:
            domain_counts["Other/Uncategorized"] += 1
            
    report = []
    header = "🚀 INTERVIEWAI - 200+ COMPANIES DOMAIN REPORT 🚀"
    report.append("=" * len(header))
    report.append(header)
    report.append("=" * len(header))
    report.append(f"Last Updated: {data['meta']['last_updated']}")
    report.append(f"Database Version: {data['meta']['version']}")
    report.append("-" * len(header))
    
    for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True):
        report.append(f"🔹 {domain:<25} : {count:>3} companies")
    
    report.append("-" * len(header))
    report.append(f"✨ TOTAL UNIQUE COMPANIES   : {len(companies)}")
    report.append("=" * len(header))
    
    final_report = "\n".join(report)
    print(final_report)
    
    # Save to a permanent report file
    with open('DOMAIN_REPORT.md', 'w', encoding='utf-8') as f:
        f.write("# Company Domain Distribution Report\n\n")
        f.write("```text\n")
        f.write(final_report)
        f.write("\n```\n")

if __name__ == "__main__":
    generate_domain_report()
