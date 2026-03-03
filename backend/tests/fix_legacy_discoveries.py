"""
Fix old-schema entries in discoveries.json.
Maps non-standard profile keys into the current standard schema.
Run once, then verify with: .\venv\Scripts\python tests\test_discovery_data.py
"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "discoveries.json")

FALLBACK_ROUNDS = {
    "Behavioral Interview": {
        "focus": "Culture fit, teamwork, and behavioral questions using STAR method.",
        "common_topics": ["Tell me about yourself", "Strengths and weaknesses", "Conflict resolution"],
        "style": "Conversational and reflective.",
        "tips": "Use the STAR method (Situation, Task, Action, Result) for every answer."
    }
}

def normalize_profile(company_name, p):
    """Normalize a legacy profile dict into the current standard schema."""
    # Try every known alias for 'name'
    name = (p.get('name') or p.get('company') or p.get('company_name')
            or p.get('companyName') or p.get('firm_name') or company_name)

    # Try every known alias for 'industry'
    industry = (p.get('industry') or p.get('sector') or p.get('domain') or "General")

    # Try every known alias for 'interview_rounds'
    rounds = p.get('interview_rounds')
    if not rounds or not isinstance(rounds, dict) or len(rounds) == 0:
        rounds = FALLBACK_ROUNDS

    # Build a clean profile — keep all existing keys but ensure required ones exist
    normalized = dict(p)  # Start with original so we don't lose data
    normalized['name']              = name
    normalized['industry']          = industry
    normalized['interview_style']   = p.get('interview_style', 'Structured and professional')
    normalized['difficulty_level']  = p.get('difficulty_level', 'Medium')
    normalized['cultural_values']   = p.get('cultural_values') or p.get('values') or []
    normalized['interview_rounds']  = rounds

    return normalized


with open(DATA_PATH, encoding='utf-8') as f:
    data = json.load(f)

fixed = 0
for e in data:
    p = e.get('interview_intelligence_profile', {})
    rounds = p.get('interview_rounds')
    needs_fix = (not p.get('name') or not p.get('industry')
                 or not rounds or not isinstance(rounds, dict) or len(rounds) == 0)
    if needs_fix:
        company_name = e.get('company_name', 'Unknown')
        e['interview_intelligence_profile'] = normalize_profile(company_name, p)
        fixed += 1
        print(f"  Fixed: {company_name}")

with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nDone. Fixed {fixed}/{len(data)} entries.")
print("Now run: .\\venv\\Scripts\\python tests\\test_discovery_data.py")
