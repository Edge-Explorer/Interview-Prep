import json
import os
import re

def merge_all_companies():
    backend_dir = r'c:\Users\ASUS\OneDrive\Desktop\Interview Prep\backend'
    data_path = os.path.join(backend_dir, 'data', 'company_profiles.json')
    
    # Scripts to extract from
    scripts = [
        'batch_add_companies.py',
        'batch_add_ai_companies.py',
        'batch_add_round8.py',
        'batch_add_round7.py',
        'batch_add_round2.py',
        'batch_add_perfect_balance.py',
        'batch_add_domain_expansion.py',
        'batch_add_domain_balancing.py'
    ]
    
    all_new_companies = {}
    
    for script in scripts:
        script_path = os.path.join(backend_dir, script)
        if not os.path.exists(script_path):
            continue
            
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # This is a bit hacky, but we can try to extract the COMPANIES_TO_ADD dict
        # using regex or just executing the script in a safe way.
        # Since these are simple scripts, we can try to exec() the part that defines COMPANIES_TO_ADD.
        try:
            # Extract the dict definition
            match = re.search(r'COMPANIES_TO_ADD = \{(.*?)\n\}', content, re.DOTALL)
            if match:
                # We need to be careful with exec. A better way is to import but they have side effects.
                # Let's try to parse it as semi-JSON if it's simple enough, or just use a temp dict.
                namespace = {}
                # Extract everything between COMPANIES_TO_ADD = { and the closing } for that dict.
                # We'll use a more robust regex or just look for the dict block.
                start_marker = 'COMPANIES_TO_ADD = {'
                start_idx = content.find(start_marker)
                if start_idx != -1:
                    # Find matching closing brace
                    brace_count = 0
                    end_idx = -1
                    for i in range(start_idx + len(start_marker) - 1, len(content)):
                        if content[i] == '{':
                            brace_count += 1
                        elif content[i] == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                end_idx = i + 1
                                break
                    if end_idx != -1:
                        dict_str = content[start_idx:end_idx]
                        exec(dict_str, {}, namespace)
                        if 'COMPANIES_TO_ADD' in namespace:
                            all_new_companies.update(namespace['COMPANIES_TO_ADD'])
        except Exception as e:
            print(f"Error parsing {script}: {e}")

    # Load existing data
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    existing_companies = data['companies']
    added_count = 0
    
    for name, info in all_new_companies.items():
        if name not in existing_companies:
            existing_companies[name] = info
            added_count += 1
            print(f"Added: {name}")
    
    data['meta']['total_companies'] = len(existing_companies)
    data['meta']['version'] = "8.2.0"
    data['meta']['last_updated'] = "2026-02-15"
    
    # Save back
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print(f"Finished. Added {added_count} new companies.")
    print(f"Total companies: {data['meta']['total_companies']}")

if __name__ == "__main__":
    merge_all_companies()
