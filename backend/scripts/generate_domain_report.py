import json
import os
from datetime import datetime

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(BACKEND_DIR, 'data')

PROFILES_PATH = os.path.join(DATA_DIR, 'company_profiles.json')
DISCOVERIES_PATH = os.path.join(DATA_DIR, 'discoveries.json')
REPORT_PATH = os.path.join(DATA_DIR, 'DOMAIN_REPORT.md')

# Domain Keywords Mapping (Refined for exact coverage)
DOMAIN_MAPPER = {
    "Engineering & Tech": ["technology", "software", "ai", "machine learning", "cybersecurity", "hardware", "internet", "e-commerce", "semiconductor", "automotive", "aerospace", "embedded", "cloud", "saas", "it services", "it consulting"],
    "Business & Management": ["management", "strategy", "hr", "administrative", "business services", "logistics", "supply chain", "consulting"],
    "Construction & Trades": ["construction", "architecture", "civil", "trades", "real estate", "infrastructure", "building"],
    "Social Services": ["non-profit", "npo", "social work", "community", "public service", "foundation", "government"],
    "Finance & Accounting": ["finance", "banking", "fintech", "accounting", "audit", "insurance", "investment", "trading", "crypto", "payments"],
    "Healthcare & Medical": ["healthcare", "medical", "pharmaceutical", "biotech", "hospital", "health", "wellness", "dental", "pharma", "diagnostics"],
    "Legal": ["legal", "law", "attorney", "compliance", "regulatory", "e-discovery", "contract automation"],
    "Science & Research": ["science", "research", "scientific", "laboratory", "rd", "physics", "biology", "chemistry"],
    "Hospitality & Tourism": ["hospitality", "tourism", "hotel", "travel", "restaurant", "events", "leisure", "aviation"],
    "Creative & Design": ["creative", "design", "media", "production", "entertainment", "fashion", "architecture (design)", "video production"],
    "Education & Training": ["education", "training", "edtech", "university", "college", "school", "teaching", "e-learning", "lms"],
    "Sales & Marketing": ["sales", "marketing", "retail", "consumer goods", "advertising", "market research", "public opinion", "digital transformation", "data services", "audience measurement"]
}

def categorize_industry(industry_str):
    if not industry_str:
        return "Other/Uncategorized"
    
    industry_lower = str(industry_str).lower()
    
    # Priority check for multi-word or specific terms
    for domain, keywords in DOMAIN_MAPPER.items():
        for keyword in keywords:
            if keyword in industry_lower:
                return domain
            
    return "Other/Uncategorized"

def generate_report():
    print("LOG: Starting Domain Distribution Analysis...")
    
    all_companies = {}
    
    if os.path.exists(PROFILES_PATH):
        try:
            with open(PROFILES_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                main_companies = data.get('companies', {})
                for name, profile in main_companies.items():
                    all_companies[name.lower()] = profile.get('industry', 'Other/Uncategorized')
        except Exception as e:
            print(f"WARNING: Could not load company_profiles.json: {e}")
                
    if os.path.exists(DISCOVERIES_PATH):
        try:
            with open(DISCOVERIES_PATH, 'r', encoding='utf-8') as f:
                discoveries = json.load(f)
                for entry in discoveries:
                    name = entry.get('company_name', 'Unknown')
                    profile_wrapper = entry.get('interview_intelligence_profile', {})
                    industry = "Other/Uncategorized"
                    if isinstance(profile_wrapper, dict):
                        industry = profile_wrapper.get('industry') or \
                                   profile_wrapper.get('company_profile', {}).get('industry') or \
                                   "Other/Uncategorized"
                    all_companies[name.lower()] = industry
        except Exception as e:
            print(f"WARNING: Could not load discoveries.json: {e}")

    domain_counts = {domain: 0 for domain in DOMAIN_MAPPER.keys()}
    domain_counts["Other/Uncategorized"] = 0
    
    for industry in all_companies.values():
        domain = categorize_industry(industry)
        domain_counts[domain] += 1
        
    total_companies = len(all_companies)
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    report_lines = [
        "# Company Domain Distribution Report",
        "",
        "```text",
        "==============================================",
        "*** INTERVIEWAI - LIVE DOMAIN REPORT ***",
        "==============================================",
        f"Last Updated: {date_str}",
        "Database Version: Agentic-Live",
        "----------------------------------------------"
    ]
    
    sorted_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)
    
    for domain, count in sorted_domains:
        if domain == "Other/Uncategorized":
            continue
        report_lines.append(f"> {domain:<25} : {count:>3} companies")
        
    report_lines.append(f"> Other/Uncategorized           : {domain_counts['Other/Uncategorized']:>3} companies")
    
    report_lines.extend([
        "----------------------------------------------",
        f"* TOTAL UNIQUE COMPANIES   : {total_companies}",
        "==============================================",
        "```",
        ""
    ])
    
    try:
        with open(REPORT_PATH, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_lines))
        print(f"SUCCESS: Report updated at {REPORT_PATH}")
        print(f"INFO: Processed {total_companies} unique companies.")
    except Exception as e:
        print(f"ERROR: Failed to write report: {e}")

if __name__ == "__main__":
    generate_report()
