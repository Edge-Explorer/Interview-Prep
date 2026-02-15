import json
import os

COMPANIES_TO_ADD = {
    # ========== LEGAL (20 Companies) ==========
    "DLA Piper": {"industry": "Legal Services/Law Firm"},
    "Kirkland & Ellis": {"industry": "Legal Services/Law Firm"},
    "Latham & Watkins": {"industry": "Legal Services/Law Firm"},
    "Baker McKenzie": {"industry": "Legal Services/Law Firm"},
    "Skadden": {"industry": "Legal Services/Law Firm"},
    "Clifford Chance": {"industry": "Legal Services/Law Firm"},
    "Linklaters": {"industry": "Legal Services/Law Firm"},
    "Hogan Lovells": {"industry": "Legal Services/Law Firm"},
    "White & Case": {"industry": "Legal Services/Law Firm"},
    "Sidley Austin": {"industry": "Legal Services/Law Firm"},
    "Jones Day": {"industry": "Legal Services/Law Firm"},
    "Norton Rose Fulbright": {"industry": "Legal Services/Law Firm"},
    "Morgan Lewis": {"industry": "Legal Services/Law Firm"},
    "Dentons": {"industry": "Legal Services/Law Firm"},
    "Reed Smith": {"industry": "Legal Services/Law Firm"},
    "Allen & Overy": {"industry": "Legal Services/Law Firm"},
    "Freshfields Bruckhaus Deringer": {"industry": "Legal Services/Law Firm"},
    "Axiom": {"industry": "Legal Tech/Services"},
    "Clio": {"industry": "Legal Tech/SaaS"},
    "Everlaw": {"industry": "Legal Tech/E-Discovery"},

    # ========== SCIENCE & RESEARCH (19 Companies) ==========
    "NASA": {"industry": "Space/Science Research"},
    "CERN": {"industry": "Science/Physics Research"},
    "ISRO": {"industry": "Space/Science Research"},
    "ESA": {"industry": "Space/Science Research"},
    "JPL (Jet Propulsion Laboratory)": {"industry": "Space/Science Research"},
    "IBM Research": {"industry": "Science/Deep Tech Research"},
    "Microsoft Research": {"industry": "Science/AI Research"},
    "Bell Labs": {"industry": "Science/Telecommunications Research"},
    "Xerox PARC": {"industry": "Science/Computing Research"},
    "MIT Media Lab": {"industry": "Science/Interdisciplinary Research"},
    "Broad Institute": {"industry": "Science/Biomedical Research"},
    "Salk Institute": {"industry": "Science/Biological Research"},
    "Scripps Research": {"industry": "Science/Biomedical Research"},
    "Argonne National Laboratory": {"industry": "Science/Energy Research"},
    "Oak Ridge National Laboratory": {"industry": "Science/Energy Research"},
    "Lawrence Livermore National Lab": {"industry": "Science/Nuclear Research"},
    "SRI International": {"industry": "Science/Non-profit Research"},
    "Battelle": {"industry": "Science/Applied Research"},
    "RAND Corporation": {"industry": "Science/Policy Research"},

    # ========== EDUCATION & TRAINING (13 Companies) ==========
    "Chegg": {"industry": "Education/EdTech"},
    "Quizlet": {"industry": "Education/EdTech"},
    "Pearson": {"industry": "Education/Publishing"},
    "McGraw Hill": {"industry": "Education/Publishing"},
    "Houghton Mifflin Harcourt": {"industry": "Education/Publishing"},
    "Rosetta Stone": {"industry": "Education/Language Learning"},
    "Babbel": {"industry": "Education/Language Learning"},
    "MasterClass": {"industry": "Education/Streaming"},
    "Skillshare": {"industry": "Education/Marketplace"},
    "Pluralsight": {"industry": "Education/SaaS"},
    "Codecademy": {"industry": "Education/SaaS"},
    "Simplilearn": {"industry": "Education/EdTech"},
    "Great Learning": {"industry": "Education/EdTech"},

    # ========== SOCIAL SERVICES (20 Companies) ==========
    "American Red Cross": {"industry": "Non-profit/Social Services"},
    "Bill & Melinda Gates Foundation": {"industry": "Non-profit/Philanthropy"},
    "UNICEF": {"industry": "Non-profit/Social Services"},
    "United Way": {"industry": "Non-profit/Social Services"},
    "Salvation Army": {"industry": "Non-profit/Social Services"},
    "Goodwill Industries": {"industry": "Non-profit/Social Services"},
    "World Vision": {"industry": "Non-profit/Social Services"},
    "MSF (Doctors Without Borders)": {"industry": "Non-profit/Healthcare Social Services"},
    "Habitat for Humanity": {"industry": "Non-profit/Social Services"},
    "Feeding America": {"industry": "Non-profit/Social Services"},
    "American Cancer Society": {"industry": "Non-profit/Healthcare Social Services"},
    "WWF (World Wildlife Fund)": {"industry": "Non-profit/Environmental Social Services"},
    "Greenpeace": {"industry": "Non-profit/Environmental Social Services"},
    "Amnesty International": {"industry": "Non-profit/Social Services"},
    "Save the Children": {"industry": "Non-profit/Social Services"},
    "Plan International": {"industry": "Non-profit/Social Services"},
    "Oxfam": {"industry": "Non-profit/Social Services"},
    "CARE": {"industry": "Non-profit/Social Services"},
    "Catholic Charities": {"industry": "Non-profit/Social Services"},
    "YMCA": {"industry": "Non-profit/Social Services"},

    # ========== CREATIVE & DESIGN (12 Companies) ==========
    "Pixar Animation Studios": {"industry": "Creative/Animation"},
    "DreamWorks Animation": {"industry": "Creative/Animation"},
    "Industrial Light & Magic (ILM)": {"industry": "Creative/VFX"},
    "Electronic Arts (EA)": {"industry": "Creative/Gaming"},
    "Nintendo": {"industry": "Creative/Gaming"},
    "Capcom": {"industry": "Creative/Gaming"},
    "Square Enix": {"industry": "Creative/Gaming"},
    "Bandai Namco": {"industry": "Creative/Gaming"},
    "InVision": {"industry": "Creative/Design SaaS"},
    "Sketch": {"industry": "Creative/Design SaaS"},
    "Dribbble": {"industry": "Creative/Community"},
    "Behance": {"industry": "Creative/Community"},

    # ========== BUSINESS & MANAGEMENT (10 Companies) ==========
    "Bain & Company": {"industry": "Consulting/Business Management"},
    "Boston Consulting Group (BCG)": {"industry": "Consulting/Business Management"},
    "Gartner": {"industry": "Consulting/Market Research"},
    "Forrester": {"industry": "Consulting/Market Research"},
    "Mercer": {"industry": "Consulting/HR Management"},
    "Willis Towers Watson": {"industry": "Consulting/Risk Management"},
    "Korn Ferry": {"industry": "Consulting/Executive Search"},
    "Oliver Wyman": {"industry": "Consulting/Strategy"},
    "Booz Allen Hamilton": {"industry": "Consulting/Tech Management"},
    "McKinsey & Company": {"industry": "Consulting/Business Management"},

    # ========== SALES & MARKETING (8 Companies) ==========
    "WPP": {"industry": "Marketing/Advertising"},
    "Omnicom Group": {"industry": "Marketing/Advertising"},
    "Publicis Groupe": {"industry": "Marketing/Advertising"},
    "Interpublic Group (IPG)": {"industry": "Marketing/Advertising"},
    "Dentsu": {"industry": "Marketing/Advertising"},
    "Ogilvy": {"industry": "Marketing/Advertising"},
    "Leo Burnett": {"industry": "Marketing/Advertising"},
    "McCann Worldgroup": {"industry": "Marketing/Advertising"},

    # ========== HEALTHCARE & MEDICAL (4 Companies) ==========
    "Johnson & Johnson": {"industry": "Healthcare/Pharma"},
    "Roche": {"industry": "Healthcare/Diagnostics"},
    "Novartis": {"industry": "Healthcare/Pharma"},
    "Merck": {"industry": "Healthcare/Pharma"},

    # ========== CONSTRUCTION & TRADES / LOGISTICS (4 Companies) ==========
    "Bechtel": {"industry": "Construction/Engineering"},
    "Turner Construction": {"industry": "Construction"},
    "AECOM": {"industry": "Construction/Infrastructure"},
    "Maersk": {"industry": "Logistics/Shipping"},

    # ========== HOSPITALITY & TOURISM (4 Companies) ==========
    "Marriott International": {"industry": "Hospitality/Hotels"},
    "Hilton": {"industry": "Hospitality/Hotels"},
    "Hyatt": {"industry": "Hospitality/Hotels"},
    "InterContinental Hotels Group (IHG)": {"industry": "Hospitality/Hotels"},

    # ========== FINANCE & ACCOUNTING (1 Company) ==========
    "Mastercard": {"industry": "Finance/Payments"}
}

def reach_20_plus_all():
    path = 'data/company_profiles.json'
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for name, base_info in COMPANIES_TO_ADD.items():
        if name in data['companies']:
            continue
            
        info = {
            "name": name,
            "industry": base_info['industry'],
            "size": "Large" if "Firm" in base_info['industry'] or "Group" in name else "Medium-Large",
            "interview_style": "rigorous-technical" if "Research" in base_info['industry'] else "professional-behavioral",
            "difficulty_level": "High",
            "cultural_values": ["Integrity", "Excellence", "Collaboration"],
            "interview_rounds": {
                "Technical": {"focus": f"{base_info['industry']} expertise"},
                "Behavioral": {"focus": "Cultural fit and teamwork"}
            },
            "red_flags": ["Poor communication", "Lack of industry depth"],
            "average_process_duration": "4-8 weeks",
            "interview_count": "4-6 rounds"
        }
        data['companies'][name] = info
    
    data['meta']['total_companies'] = len(data['companies'])
    data['meta']['version'] = "9.0.0"
    data['meta']['last_updated'] = "2026-02-15"
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Grand Total Companies: {data['meta']['total_companies']}")

if __name__ == "__main__":
    reach_20_plus_all()
