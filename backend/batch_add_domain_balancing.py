"""
Batch script to balance domain coverage - Round 5
Focus: Gaming, Cybersecurity, Healthcare, Travel, Media, Food Delivery, EdTech
"""

import json
import os

# ============================================
# COMPANIES TO ADD - ROUND 5 (DOMAIN BALANCING)
# ============================================

COMPANIES_TO_ADD = {
    # ========== MORE GAMING ==========
    "Unity Technologies": {
        "name": "Unity Technologies",
        "industry": "Gaming/Game Engine",
        "size": "Medium (5000-10000)",
        "interview_style": "game-engine-focused",
        "difficulty_level": "High",
        "cultural_values": [
            "Democratize game development",
            "Innovation",
            "Collaboration",
            "Excellence",
            "User focus"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Game engine, C#, graphics, cross-platform development",
                "common_topics": ["Unity Engine", "C#", "Graphics", "Game optimization", "Cross-platform"],
                "style": "Game development focus, C# expertise",
                "tips": "Know Unity Engine. Strong C# required. Graphics and optimization. Cross-platform development."
            },
            "Behavioral": {
                "focus": "Democratization, innovation, collaboration",
                "common_questions": [
                    "Why Unity? Experience with Unity Engine?",
                    "Tell me about a game optimization project",
                    "Describe your game development experience",
                    "How do you approach cross-platform development?"
                ],
                "style": "Game-focused, developer empathy"
            },
            "System Design": {
                "focus": "Game engine, asset pipeline, cross-platform",
                "common_topics": ["Design asset pipeline", "Design rendering system", "Design cross-platform framework"],
                "style": "Focus on developer experience and performance"
            }
        },
        "red_flags": ["Weak C#", "No game development experience", "Not performance-focused"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Roblox": {
        "name": "Roblox",
        "industry": "Gaming/UGC Platform",
        "size": "Medium (1000-5000)",
        "interview_style": "platform-and-community",
        "difficulty_level": "High",
        "cultural_values": [
            "Respect the community",
            "Take the long view",
            "Work hard, have fun",
            "Be bold",
            "Collaborate"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "UGC platform, game engine, Lua, safety, scale",
                "common_topics": ["Platform engineering", "Lua", "Content moderation", "Safety systems", "Scale"],
                "style": "Platform focus, safety-conscious",
                "tips": "Understand UGC platforms. Discuss safety and moderation. Scale challenges. Community focus."
            },
            "Behavioral": {
                "focus": "Community respect, safety, long-term thinking",
                "common_questions": [
                    "How do you ensure platform safety?",
                    "Tell me about building for creators",
                    "Describe your approach to UGC moderation",
                    "How do you think about community?"
                ],
                "style": "Community-focused, safety-first"
            },
            "System Design": {
                "focus": "UGC platform, moderation, safety, scale",
                "common_topics": ["Design UGC platform", "Design content moderation", "Design creator tools"],
                "style": "Focus on safety and community"
            }
        },
        "red_flags": ["Not safety-conscious", "Ignoring community", "Weak platform knowledge"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "5-6 rounds"
    },
    
    # ========== MORE CYBERSECURITY ==========
    "Okta": {
        "name": "Okta",
        "industry": "Cybersecurity/Identity",
        "size": "Medium (5000-10000)",
        "interview_style": "identity-and-security",
        "difficulty_level": "High",
        "cultural_values": [
            "Customer success",
            "Innovation",
            "Integrity",
            "Transparency",
            "Inclusion"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Identity management, SSO, authentication, security",
                "common_topics": ["OAuth/OIDC", "SAML", "SSO", "MFA", "Identity security"],
                "style": "Security and identity focus",
                "tips": "Know identity protocols. Discuss OAuth/OIDC. SSO and MFA. Security best practices."
            },
            "Behavioral": {
                "focus": "Customer success, integrity, transparency",
                "common_questions": [
                    "How do you approach identity security?",
                    "Tell me about implementing SSO",
                    "Describe your security philosophy",
                    "How do you handle customer needs?"
                ],
                "style": "Customer-focused, security-conscious"
            },
            "System Design": {
                "focus": "Identity platform, SSO, authentication",
                "common_topics": ["Design SSO system", "Design MFA", "Design identity management"],
                "style": "Focus on security and scalability"
            }
        },
        "red_flags": ["Weak identity knowledge", "Not security-conscious", "Ignoring customer needs"],
        "average_process_duration": "5-6 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Zscaler": {
        "name": "Zscaler",
        "industry": "Cybersecurity/Cloud Security",
        "size": "Medium (5000-10000)",
        "interview_style": "cloud-security-focused",
        "difficulty_level": "High",
        "cultural_values": [
            "Customer obsession",
            "Innovation",
            "Teamwork",
            "Integrity",
            "Excellence"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Cloud security, zero trust, networking, threat detection",
                "common_topics": ["Zero trust", "Cloud security", "Network security", "Threat prevention", "SSL inspection"],
                "style": "Cloud security focus, zero trust mindset",
                "tips": "Know zero trust architecture. Cloud security. Network protocols. Threat landscape."
            },
            "Behavioral": {
                "focus": "Customer obsession, innovation, teamwork",
                "common_questions": [
                    "How do you approach zero trust?",
                    "Tell me about cloud security challenges",
                    "Describe your threat detection experience",
                    "How do you ensure security at scale?"
                ],
                "style": "Security-focused, customer-centric"
            },
            "System Design": {
                "focus": "Cloud security, zero trust, threat detection",
                "common_topics": ["Design zero trust architecture", "Design cloud security platform", "Design threat detection"],
                "style": "Focus on cloud-native security"
            }
        },
        "red_flags": ["Weak cloud security knowledge", "Not zero trust minded", "Ignoring threats"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "4-5 rounds"
    },
    
    # ========== MORE HEALTHCARE TECH ==========
    "Epic Systems": {
        "name": "Epic Systems",
        "industry": "Healthcare/EHR",
        "size": "Large (>10000)",
        "interview_style": "healthcare-systems-focused",
        "difficulty_level": "Medium-High",
        "cultural_values": [
            "Patient care",
            "Innovation",
            "Integrity",
            "Excellence",
            "Collaboration"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Healthcare systems, EHR, databases, integration, compliance",
                "common_topics": ["EHR systems", "HL7/FHIR", "Healthcare workflows", "Database design", "HIPAA"],
                "style": "Healthcare domain focus, compliance-heavy",
                "tips": "Understand healthcare workflows. Know HL7/FHIR. HIPAA compliance. Database expertise."
            },
            "Behavioral": {
                "focus": "Patient care, integrity, excellence",
                "common_questions": [
                    "Why healthcare? Why Epic?",
                    "Tell me about building healthcare systems",
                    "Describe your approach to patient data",
                    "How do you ensure system reliability?"
                ],
                "style": "Patient-focused, mission-driven"
            },
            "System Design": {
                "focus": "EHR systems, healthcare integration, compliance",
                "common_topics": ["Design EHR system", "Design HL7 integration", "Design clinical workflows"],
                "style": "Focus on patient safety and compliance"
            }
        },
        "red_flags": ["Not patient-focused", "Weak healthcare knowledge", "Ignoring compliance"],
        "average_process_duration": "6-8 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Cerner (Oracle Health)": {
        "name": "Cerner (Oracle Health)",
        "industry": "Healthcare/Health IT",
        "size": "Large (>20000)",
        "interview_style": "enterprise-healthcare",
        "difficulty_level": "Medium",
        "cultural_values": [
            "Patient first",
            "Innovation",
            "Integrity",
            "Teamwork",
            "Excellence"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Healthcare IT, EHR, interoperability, databases",
                "common_topics": ["Healthcare IT", "Interoperability", "Clinical systems", "Database", "Integration"],
                "style": "Enterprise healthcare focus",
                "tips": "Know healthcare IT. Discuss interoperability. Clinical workflows. Enterprise scale."
            },
            "Behavioral": {
                "focus": "Patient focus, teamwork, integrity",
                "common_questions": [
                    "How do you approach healthcare IT?",
                    "Tell me about clinical system integration",
                    "Describe your healthcare experience",
                    "How do you ensure data accuracy?"
                ],
                "style": "Patient-focused, enterprise mindset"
            },
            "System Design": {
                "focus": "Healthcare IT, interoperability, clinical systems",
                "common_topics": ["Design clinical system", "Design interoperability", "Design patient portal"],
                "style": "Focus on clinical workflows and compliance"
            }
        },
        "red_flags": ["Weak healthcare knowledge", "Not patient-focused", "Ignoring compliance"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "3-4 rounds"
    },
    
    # ========== MORE TRAVEL ==========
    "Expedia Group": {
        "name": "Expedia Group",
        "industry": "Travel/E-commerce",
        "size": "Large (>15000)",
        "interview_style": "travel-platform-focused",
        "difficulty_level": "High",
        "cultural_values": [
            "Customer first",
            "Innovation",
            "Inclusion",
            "Integrity",
            "Collaboration"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Travel platform, search, inventory, pricing, mobile",
                "common_topics": ["Search algorithms", "Inventory systems", "Dynamic pricing", "Mobile apps", "Microservices"],
                "style": "Travel domain focus, scale emphasis",
                "tips": "Understand travel domain. Discuss search and inventory. Dynamic pricing. Mobile experience."
            },
            "Behavioral": {
                "focus": "Customer focus, innovation, collaboration",
                "common_questions": [
                    "How would you improve travel booking?",
                    "Tell me about building search systems",
                    "Describe your approach to pricing",
                    "How do you handle inventory?"
                ],
                "style": "Customer-focused, travel-oriented"
            },
            "System Design": {
                "focus": "Travel platform, search, inventory, pricing",
                "common_topics": ["Design travel search", "Design inventory system", "Design dynamic pricing"],
                "style": "Focus on travel domain and scale"
            }
        },
        "red_flags": ["Weak search knowledge", "Not customer-focused", "Ignoring travel domain"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Airbnb": {
        "name": "Airbnb",
        "industry": "Travel/Marketplace",
        "size": "Medium (5000-10000)",
        "interview_style": "product-and-culture-heavy",
        "difficulty_level": "Very High",
        "cultural_values": [
            "Champion the mission",
            "Be a host",
            "Embrace the adventure",
            "Be a cereal entrepreneur",
            "Simplify"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Marketplace, trust & safety, search, mobile, product engineering",
                "common_topics": ["Marketplace dynamics", "Trust & safety", "Search ranking", "Mobile apps", "Product thinking"],
                "style": "Product-focused, culture-heavy, high bar",
                "tips": "Know marketplace dynamics. Discuss trust & safety. Product thinking critical. Culture fit very important."
            },
            "Behavioral": {
                "focus": "Mission alignment, host mentality, culture fit",
                "common_questions": [
                    "Why Airbnb? Tell me about a travel experience",
                    "How do you build trust in a marketplace?",
                    "Describe a time you championed a mission",
                    "How do you approach product thinking?"
                ],
                "style": "Culture-heavy, mission-driven, storytelling valued"
            },
            "System Design": {
                "focus": "Marketplace, trust & safety, search, recommendations",
                "common_topics": ["Design marketplace", "Design trust & safety", "Design search ranking"],
                "style": "Focus on marketplace and trust"
            }
        },
        "red_flags": ["Not mission-aligned", "Weak culture fit", "Ignoring trust & safety", "No product sense"],
        "average_process_duration": "6-10 weeks",
        "interview_count": "6-8 rounds"
    },
    
    # ========== MORE MEDIA/ENTERTAINMENT ==========
    "Twitch": {
        "name": "Twitch",
        "industry": "Media/Live Streaming",
        "size": "Medium (1000-5000)",
        "interview_style": "streaming-and-community",
        "difficulty_level": "High",
        "cultural_values": [
            "Community first",
            "Innovation",
            "Passion",
            "Ownership",
            "Inclusion"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Live streaming, real-time chat, video infrastructure, community",
                "common_topics": ["Video streaming", "Real-time chat", "CDN", "Community moderation", "Low latency"],
                "style": "Streaming focus, community-oriented",
                "tips": "Know live streaming tech. Discuss low-latency systems. Community features. Video infrastructure."
            },
            "Behavioral": {
                "focus": "Community focus, passion, ownership",
                "common_questions": [
                    "Why Twitch? Do you stream or watch streams?",
                    "How would you improve streamer experience?",
                    "Tell me about building community features",
                    "Describe your approach to moderation"
                ],
                "style": "Community-focused, passion for streaming valued"
            },
            "System Design": {
                "focus": "Live streaming, real-time chat, community",
                "common_topics": ["Design live streaming", "Design chat system", "Design moderation tools"],
                "style": "Focus on low-latency and community"
            }
        },
        "red_flags": ["Not community-focused", "Weak streaming knowledge", "No passion for platform"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "TikTok (ByteDance)": {
        "name": "TikTok (ByteDance)",
        "industry": "Social Media/Short Video",
        "size": "Large (>100000)",
        "interview_style": "algorithm-and-scale",
        "difficulty_level": "Very High",
        "cultural_values": [
            "Always day one",
            "Seek truth and be pragmatic",
            "Be courageous and aim for the highest",
            "Be open and humble",
            "Be candid and clear"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Recommendation algorithms, video processing, mobile, global scale",
                "common_topics": ["Recommendation systems", "Video processing", "Mobile apps", "Distributed systems", "ML"],
                "style": "Algorithm-heavy, scale focus, very rigorous",
                "tips": "Know recommendation algorithms. Discuss video processing. Mobile optimization. Global scale challenges."
            },
            "Behavioral": {
                "focus": "Pragmatism, courage, humility, candor",
                "common_questions": [
                    "How would you improve TikTok's algorithm?",
                    "Tell me about building at global scale",
                    "Describe your approach to recommendations",
                    "How do you handle ambiguity?"
                ],
                "style": "Fast-paced, pragmatic, high standards"
            },
            "System Design": {
                "focus": "Recommendation engine, video platform, global scale",
                "common_topics": ["Design recommendation system", "Design video platform", "Design global CDN"],
                "style": "Focus on algorithms and massive scale"
            }
        },
        "red_flags": ["Weak ML/algorithms", "Not pragmatic", "Ignoring scale", "Slow execution"],
        "average_process_duration": "6-8 weeks",
        "interview_count": "5-7 rounds"
    },
    
    # ========== FOOD DELIVERY (NEW DOMAIN) ==========
    "DoorDash": {
        "name": "DoorDash",
        "industry": "Food Delivery/Logistics",
        "size": "Medium (5000-10000)",
        "interview_style": "logistics-and-marketplace",
        "difficulty_level": "High",
        "cultural_values": [
            "Delight customers",
            "Be an owner",
            "Act with urgency",
            "Win together",
            "Truth seeking"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Logistics, marketplace, routing, real-time matching, mobile",
                "common_topics": ["Routing algorithms", "Dasher matching", "ETA prediction", "Mobile apps", "Marketplace"],
                "style": "Logistics focus, practical problem-solving",
                "tips": "Understand three-sided marketplace. Discuss routing and matching. Real-time systems. Mobile-first."
            },
            "Behavioral": {
                "focus": "Ownership, urgency, customer delight",
                "common_questions": [
                    "How would you improve delivery times?",
                    "Tell me about optimizing logistics",
                    "Describe your approach to marketplaces",
                    "How do you act with urgency?"
                ],
                "style": "Action-oriented, ownership culture"
            },
            "System Design": {
                "focus": "Food delivery, routing, matching, marketplace",
                "common_topics": ["Design delivery matching", "Design routing system", "Design marketplace"],
                "style": "Focus on logistics and real-time optimization"
            }
        },
        "red_flags": ["Weak logistics knowledge", "Slow execution", "Not customer-focused"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "5-6 rounds"
    },
    
    "Uber Eats": {
        "name": "Uber Eats",
        "industry": "Food Delivery/Marketplace",
        "size": "Large (part of Uber)",
        "interview_style": "marketplace-and-logistics",
        "difficulty_level": "High",
        "cultural_values": [
            "Customer obsession",
            "Make magic",
            "Big bold bets",
            "Move fast",
            "Be an owner"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Marketplace, logistics, routing, real-time, mobile",
                "common_topics": ["Marketplace dynamics", "Routing", "Real-time matching", "Mobile apps", "Surge pricing"],
                "style": "Fast-paced, marketplace focus",
                "tips": "Understand marketplace dynamics. Discuss routing and matching. Real-time systems. Uber culture."
            },
            "Behavioral": {
                "focus": "Customer obsession, ownership, speed",
                "common_questions": [
                    "How would you improve Uber Eats?",
                    "Tell me about marketplace optimization",
                    "Describe your approach to logistics",
                    "How do you move fast?"
                ],
                "style": "Fast-paced, ownership-driven"
            },
            "System Design": {
                "focus": "Food delivery, marketplace, routing, real-time",
                "common_topics": ["Design delivery system", "Design marketplace", "Design surge pricing"],
                "style": "Focus on marketplace and logistics"
            }
        },
        "red_flags": ["Slow execution", "Weak marketplace knowledge", "Not customer-focused"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "4-5 rounds"
    }
}

# ============================================
# BATCH ADD FUNCTION
# ============================================

def batch_add_companies():
    """Add all domain-balancing companies to the database"""
    
    # Load existing data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'data', 'company_profiles.json')
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("="*60)
    print("BATCH ADDING COMPANIES - ROUND 5 (DOMAIN BALANCING)")
    print("="*60)
    print(f"\nCompanies to add: {len(COMPANIES_TO_ADD)}")
    print("\nBalancing domains:")
    print("  - Gaming: +2 (Unity, Roblox)")
    print("  - Cybersecurity: +2 (Okta, Zscaler)")
    print("  - Healthcare: +2 (Epic Systems, Cerner)")
    print("  - Travel: +2 (Expedia, Airbnb)")
    print("  - Media: +3 (Twitch, TikTok)")
    print("  - Food Delivery: +2 (DoorDash, Uber Eats) [NEW]")
    
    # Check for duplicates
    duplicates = []
    for company_name in COMPANIES_TO_ADD.keys():
        if company_name in data['companies']:
            duplicates.append(company_name)
    
    if duplicates:
        print(f"\n⚠️  Warning: {len(duplicates)} companies already exist:")
        for dup in duplicates:
            print(f"   - {dup}")
        overwrite = input("\nOverwrite existing companies? (yes/no): ").lower()
        if overwrite != 'yes':
            print("❌ Cancelled. No changes made.")
            return
    
    # Add all companies
    added_count = 0
    for company_name, company_data in COMPANIES_TO_ADD.items():
        data['companies'][company_name] = company_data
        added_count += 1
        print(f"✅ Added: {company_name}")
    
    # Update metadata
    data['meta']['total_companies'] = len(data['companies'])
    data['meta']['version'] = "5.0.0"
    
    # Save updated data
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"✅ Successfully added {added_count} companies!")
    print(f"📊 Total companies now: {data['meta']['total_companies']}")
    print(f"{'='*60}")
    print(f"\n💡 Test it by running: python test_company_intel.py")

if __name__ == "__main__":
    batch_add_companies()
