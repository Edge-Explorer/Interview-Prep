import json
import os

def analyze_domains():
    data_path = 'data/company_profiles.json'
    if not os.path.exists(data_path):
        print("File not found")
        return

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Define domain mapping
    domain_counts = {
        "AI / Machine Learning": 0,
        "Gaming & Entertainment": 0,
        "Healthcare & Medical": 0,
        "Cybersecurity": 0,
        "Media & Social Media": 0,
        "Food Delivery & Logistics": 0,
        "Travel & Hospitality": 0,
        "Finance & Fintech": 0,
        "Consulting & Services": 0,
        "Big Tech / FAANG": 0,
        "Enterprise & DevTools": 0
    }

    faang_list = ["google", "amazon", "microsoft", "meta", "apple", "netflix", "nvidia", "oracle", "ibm", "uber", "salesforce", "adobe"]

    for company_id, company in data['companies'].items():
        name = company.get('name', '').lower()
        industry = company.get('industry', '').lower()
        
        # Priority mapping
        if any(x in industry for x in ['ai', 'intelligence', 'machine learning']):
            domain_counts["AI / Machine Learning"] += 1
        elif any(x in industry for x in ['gaming', 'game']):
            domain_counts["Gaming & Entertainment"] += 1
        elif any(x in industry for x in ['health', 'medical', 'hospital', 'pharmacy', 'oncology', 'care']):
            domain_counts["Healthcare & Medical"] += 1
        elif any(x in industry for x in ['security', 'cyber', 'identity']):
            domain_counts["Cybersecurity"] += 1
        elif any(x in industry for x in ['media', 'streaming', 'video', 'social', 'music', 'communication']):
            domain_counts["Media & Social Media"] += 1
        elif any(x in industry for x in ['food', 'delivery', 'logistics', 'marketplace']) and not "travel" in industry:
            domain_counts["Food Delivery & Logistics"] += 1
        elif any(x in industry for x in ['travel', 'booking', 'ota', 'hospitality', 'metasearch']):
            domain_counts["Travel & Hospitality"] += 1
        elif any(x in industry for x in ['finance', 'fintech', 'bank', 'quant', 'trading']):
            domain_counts["Finance & Fintech"] += 1
        elif any(x in industry for x in ['consulting', 'services', 'it services']):
            domain_counts["Consulting & Services"] += 1
        elif any(x in name for x in faang_list):
            domain_counts["Big Tech / FAANG"] += 1
        else:
            domain_counts["Enterprise & DevTools"] += 1

    print("-" * 45)
    print(f"{'DOMAIN':<30} | {'COUNT':<5}")
    print("-" * 45)
    total = 0
    for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{domain:<30} | {count:<5}")
        total += count
    print("-" * 45)
    print(f"{'TOTAL COMPANIES':<30} | {total:<5}")
    print("-" * 45)

if __name__ == "__main__":
    analyze_domains()
