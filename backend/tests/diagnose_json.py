"""Quick diagnostic: finds all bad entries in discoveries.json"""
import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "discoveries.json")

with open(DATA_PATH, encoding='utf-8') as f:
    data = json.load(f)

bad = []
for i, e in enumerate(data):
    p = e.get('interview_intelligence_profile', {})
    rounds = p.get('interview_rounds')
    issues = []
    if not p.get('name'):     issues.append('missing_name')
    if not p.get('industry'): issues.append('missing_industry')
    if not rounds or not isinstance(rounds, dict) or len(rounds) == 0:
        issues.append('missing_rounds')
    if issues:
        bad.append((i, e.get('company_name', 'UNKNOWN'), issues, list(p.keys())))

print(f"Total entries: {len(data)}")
print(f"Bad entries: {len(bad)}\n")
for idx, name, issues, keys in bad:
    print(f"  Entry #{idx}: {name}")
    print(f"    Issues: {issues}")
    print(f"    Profile keys: {keys}")
    print()
