"""
Batch script to add specific requested companies and more global leaders
"""
import json
import os
import sys

# Set encoding for Windows terminal output to avoid UnicodeEncodeError
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============================================
# COMPANIES TO ADD - ROUND 7 (SPECIFIC REQUESTS)
# ============================================

COMPANIES_TO_ADD = {
    # ========== HEALTHCARE (Specific Indian Requests) ==========
    "Tata Memorial Centre": {
        "name": "Tata Memorial Centre",
        "industry": "Healthcare/Oncology",
        "size": "Large (1000-5000)",
        "interview_style": "medical-research-excellence",
        "difficulty_level": "High",
        "cultural_values": ["Patient care", "Cancer research", "Excellence", "Compassion", "Integrity"],
        "interview_rounds": {
            "Technical": {
                "focus": "Medical research, oncology, patient care, medical technology",
                "common_topics": ["Oncology", "Cancer research", "Patient management", "Medical ethics", "Research methodology"],
                "style": "Highly academic and clinical excellence focused",
                "tips": "Show deep passion for cancer research. Discuss medical ethics and patient empathy. Academic rigor is key."
            },
            "Behavioral": {
                "focus": "Empathy, patient care, mission-driven",
                "common_questions": ["Why Tata Memorial?", "Tell me about a time you showed empathy", "How do you handle high-pressure medical situations?"],
                "style": "Passion-driven and empathy-focused"
            }
        },
        "red_flags": ["Lack of empathy", "Weak research background", "Not mission-aligned"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "3-4 rounds"
    },
    
    "KEM Hospital": {
        "name": "KEM Hospital",
        "industry": "Healthcare/Academic",
        "size": "Large (5000-10000)",
        "interview_style": "clinical-and-public-health",
        "difficulty_level": "High",
        "cultural_values": ["Public service", "Clinical excellence", "Academic rigor", "Integrity", "Collaboration"],
        "interview_rounds": {
            "Technical": {
                "focus": "Clinical practice, public health, medical residency/fellowship",
                "common_topics": ["Clinical diagnosis", "Public health infrastructure", "Emergency care", "Medical ethics"],
                "style": "Practical and clinical focus",
                "tips": "Focus on high-volume clinical experience. Discuss public health commitment. Clinical accuracy is baseline."
            }
        },
        "red_flags": ["Low clinical accuracy", "Poor communication", "Weak commitment to public service"],
        "average_process_duration": "4-8 weeks",
        "interview_count": "3 rounds"
    },

    "Apollo Hospitals": {
        "name": "Apollo Hospitals",
        "industry": "Healthcare/Hospital Chain",
        "size": "Large (>50000)",
        "interview_style": "corporate-healthcare",
        "difficulty_level": "Medium-High",
        "cultural_values": ["Patient first", "Innovation", "Operational excellence", "Integrity"],
        "interview_rounds": {
            "Technical": {
                "focus": "Healthcare operations, IT, patient experience, clinical workflows",
                "common_topics": ["Hospital management systems", "Patient workflows", "Healthcare IT", "Quality standards"],
                "tips": "Focus on scale and operational efficiency in healthcare."
            }
        },
        "red_flags": ["Weak operational knowledge", "Poor patient focus"],
        "average_process_duration": "3-5 weeks",
        "interview_count": "3-4 rounds"
    },

    # ========== GAMING (Worldwide Giants) ==========
    "Nintendo": {
        "name": "Nintendo",
        "industry": "Gaming/Entertainment",
        "size": "Large (6000-7000)",
        "interview_style": "creative-and-polished",
        "difficulty_level": "Very High",
        "cultural_values": ["Innovation through intuition", "Quality above all", "Fun for all", "Polished experience"],
        "interview_rounds": {
            "Technical": {
                "focus": "Game feel, hardware-software integration, C++, quality",
                "common_topics": ["Low-level programming", "Optimization", "Game feel", "Input latency"],
                "style": "Focus on 'Nintendo Polish' and innovation",
                "tips": "Show understanding of what makes a game 'fun'. Nintendo values distinct, unique ideas."
            }
        },
        "red_flags": ["Lack of creativity", "Ignoring game feel", "Generic ideas"],
        "average_process_duration": "6-10 weeks",
        "interview_count": "5-6 rounds"
    },

    "SEGA": {
        "name": "SEGA",
        "industry": "Gaming/Arcade & Console",
        "size": "Medium (3000-5000)",
        "interview_style": "legacy-and-innovation",
        "difficulty_level": "High",
        "cultural_values": ["Constant innovation", "Speed", "Quality", "Legacy"],
        "interview_rounds": {
            "Technical": {
                "focus": "Arcade systems, engine development, physics, multiplayer",
                "common_topics": ["Real-time physics", "Arcade hardware", "Multiplayer", "Engine code"]
            }
        },
        "red_flags": ["Weak physics knowledge", "No passion for SEGA IP"],
        "average_process_duration": "4-7 weeks",
        "interview_count": "4-5 rounds"
    },

    # ========== CYBERSECURITY (Target: 10+) ==========
    "CrowdStrike": {
        "name": "CrowdStrike",
        "industry": "Cybersecurity/Endpoint",
        "size": "Large (7000-8000)",
        "interview_style": "adversary-focused",
        "difficulty_level": "Very High",
        "cultural_values": ["Stop breaches", "Customer first", "Innovation", "Speed"],
        "interview_rounds": {
            "Technical": {
                "focus": "Endpoint detection, kernel-level coding, threat hunting, Go/C++",
                "common_topics": ["OS internals", "Malware analysis", "Threat intelligence", "Distributed systems"],
                "style": "Adversary-driven, very deep technical expectations"
            }
        },
        "red_flags": ["Weak OS internals knowledge", "Slow response to threat scenarios"],
        "average_process_duration": "5-8 weeks",
        "interview_count": "5-6 rounds"
    },

    "FireEye (Mandiant)": {
        "name": "FireEye (Mandiant)",
        "industry": "Cybersecurity/Incident Response",
        "size": "Medium (2000-3000)",
        "interview_style": "investigative-excellence",
        "difficulty_level": "Very High",
        "cultural_values": ["Investigation", "Truth seeking", "Public service", "Expertise"],
        "interview_rounds": {
            "Technical": {
                "focus": "Incident response, forensic analysis, malware investigation",
                "common_topics": ["Digitals forensics", "Memory analysis", "Log auditing", "Malware reverse engineering"]
            }
        },
        "red_flags": ["Poor attention to detail", "Weak forensic fundamentals"],
        "average_process_duration": "6-8 weeks",
        "interview_count": "5-6 rounds"
    },

    # ========== MORE INDIAN TECH GIANTS ==========
    "HCLTech": {
        "name": "HCLTech",
        "industry": "IT Services/Products",
        "size": "Large (>200000)",
        "interview_style": "consultative-and-delivery",
        "difficulty_level": "Medium",
        "cultural_values": ["Ideapreneurship", "Relationship beyond the contract", "Trust", "Transparency"],
        "interview_rounds": {
            "Technical": {
                "focus": "Full stack, cloud, infrastructure, enterprise tech",
                "common_topics": ["Java/Spring", "React", "Cloud migration", "DevOps"]
            }
        },
        "red_flags": ["Lack of ownership", "Weak foundational coding"],
        "average_process_duration": "3-5 weeks",
        "interview_count": "3-4 rounds"
    },

    "Tech Mahindra": {
        "name": "Tech Mahindra",
        "industry": "IT Services/Telecom",
        "size": "Large (>150000)",
        "interview_style": "telecom-and-enterprise",
        "difficulty_level": "Medium",
        "cultural_values": ["Rise", "Accepting no limits", "Alternative thinking", "Driving positive change"],
        "interview_rounds": {
            "Technical": {
                "focus": "5G, Telecom, cloud, data analytics",
                "common_topics": ["Networking", "Telecom protocols", "Cloud infrastructure", "Python/Data"]
            }
        },
        "red_flags": ["Resistant to change", "Weak telecom basics"],
        "average_process_duration": "3-5 weeks",
        "interview_count": "3-4 rounds"
    }
}

def batch_add_companies():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'data', 'company_profiles.json')
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("="*60)
    print("BATCH ADDING COMPANIES - ROUND 7")
    print("="*60)
    
    added_count = 0
    for company_name, company_data in COMPANIES_TO_ADD.items():
        if company_name not in data['companies']:
            data['companies'][company_name] = company_data
            added_count += 1
            print(f"✅ Added: {company_name}")
        else:
            print(f"⏩ Skipping (Exists): {company_name}")
    
    data['meta']['total_companies'] = len(data['companies'])
    data['meta']['version'] = "7.0.0"
    
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"\nSuccessfully added {added_count} companies!")
    print(f"Total companies now: {data['meta']['total_companies']}")

if __name__ == "__main__":
    batch_add_companies()
