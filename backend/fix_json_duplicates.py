import json
import os

def sanitize_json():
    filepath = r'c:\Users\ASUS\OneDrive\Desktop\Interview Prep\backend\data\company_profiles.json'
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    # Load data - Python's json.load will automatically handle duplicate keys in the same object
    # (it keeps the last one).
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            # We can't use json.load directly if we want to BE SURE about duplicates
            # actually if the file has duplicate keys at the same level, json.load
            # will just pick the last one.
            data = json.load(f)
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return

    # Let's ensure the total_companies meta matches the actual count
    company_count = len(data['companies'])
    data['meta']['total_companies'] = company_count
    
    # Save back - this will produce a clean file without duplicate keys
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Sanitized {filepath}")
    print(f"Total companies: {company_count}")

if __name__ == "__main__":
    sanitize_json()
