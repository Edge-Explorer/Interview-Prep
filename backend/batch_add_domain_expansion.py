"""
Batch script to add companies across MORE domains - Round 4
Focus: E-commerce, Gaming, Cybersecurity, Cloud, Media/Entertainment, Healthcare Tech, etc.
"""

import json
import os

# ============================================
# COMPANIES TO ADD - ROUND 4 (DOMAIN EXPANSION)
# ============================================

COMPANIES_TO_ADD = {
    # ========== E-COMMERCE & RETAIL ==========
    "Shopee": {
        "name": "Shopee",
        "industry": "E-commerce/Marketplace",
        "size": "Large (>10000)",
        "interview_style": "scale-and-mobile-first",
        "difficulty_level": "High",
        "cultural_values": [
            "Customer obsession",
            "Speed",
            "Innovation",
            "Ownership",
            "Teamwork"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "E-commerce, mobile-first, Southeast Asia scale, real-time systems",
                "common_topics": ["Mobile optimization", "E-commerce systems", "Real-time inventory", "Payment systems"],
                "style": "Fast-paced, focus on scale and mobile",
                "tips": "Think Southeast Asia scale. Mobile-first mindset. Discuss flash sales and inventory."
            },
            "Behavioral": {
                "focus": "Speed, customer obsession, ownership",
                "common_questions": [
                    "How would you handle flash sale traffic?",
                    "Tell me about optimizing for mobile",
                    "Describe your approach to e-commerce"
                ],
                "style": "Action-oriented, focus on execution"
            },
            "System Design": {
                "focus": "E-commerce platform, flash sales, mobile-first",
                "common_topics": ["Design flash sale system", "Design inventory management", "Design payment gateway"],
                "style": "Focus on scale and mobile experience"
            }
        },
        "red_flags": ["Not mobile-first", "Slow execution", "Ignoring scale challenges"],
        "average_process_duration": "3-4 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Instacart": {
        "name": "Instacart",
        "industry": "E-commerce/Grocery Delivery",
        "size": "Medium (1000-5000)",
        "interview_style": "logistics-and-marketplace",
        "difficulty_level": "High",
        "cultural_values": [
            "Customer obsession",
            "Bias for action",
            "Ownership",
            "Innovation",
            "Collaboration"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Marketplace, logistics, real-time matching, mobile",
                "common_topics": ["Shopper matching", "Routing algorithms", "Inventory prediction", "Mobile apps"],
                "style": "Practical problem-solving, marketplace focus",
                "tips": "Understand two-sided marketplace. Discuss logistics and routing. Real-time systems."
            },
            "Behavioral": {
                "focus": "Customer obsession, bias for action, ownership",
                "common_questions": [
                    "How would you improve shopper efficiency?",
                    "Tell me about a marketplace problem you solved",
                    "Describe your approach to logistics"
                ],
                "style": "Fast-paced, customer-focused"
            },
            "System Design": {
                "focus": "Marketplace, logistics, real-time matching",
                "common_topics": ["Design shopper matching", "Design delivery routing", "Design inventory system"],
                "style": "Focus on marketplace dynamics and logistics"
            }
        },
        "red_flags": ["Not understanding marketplaces", "Ignoring logistics", "Slow execution"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "4-5 rounds"
    },
    
    # ========== GAMING ==========
    "Riot Games": {
        "name": "Riot Games",
        "industry": "Gaming/Entertainment",
        "size": "Medium (5000-10000)",
        "interview_style": "player-focused-and-technical",
        "difficulty_level": "High",
        "cultural_values": [
            "Player experience first",
            "Dare to dream",
            "Thrive together",
            "Challenge convention",
            "Stay hungry, stay humble"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Game development, real-time systems, C++/C#, networking",
                "common_topics": ["Game engines", "Networking", "Real-time systems", "Anti-cheat", "Performance"],
                "style": "Gaming-focused, player experience emphasis",
                "tips": "Know gaming industry. Discuss player experience. Real-time networking. Anti-cheat systems."
            },
            "Behavioral": {
                "focus": "Player focus, passion for gaming, collaboration",
                "common_questions": [
                    "Why Riot? What games do you play?",
                    "How would you improve League of Legends?",
                    "Tell me about a time you put users first",
                    "Describe your gaming background"
                ],
                "style": "Gamer-focused, passion-driven"
            },
            "System Design": {
                "focus": "Game systems, matchmaking, anti-cheat, real-time",
                "common_topics": ["Design matchmaking system", "Design anti-cheat", "Design game server architecture"],
                "style": "Focus on player experience and real-time performance"
            }
        },
        "red_flags": ["Not a gamer", "Ignoring player experience", "Weak real-time systems knowledge"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "5-6 rounds"
    },
    
    "Epic Games": {
        "name": "Epic Games",
        "industry": "Gaming/Game Engine",
        "size": "Medium (1000-5000)",
        "interview_style": "technical-excellence-gaming",
        "difficulty_level": "Very High",
        "cultural_values": [
            "Innovation",
            "Excellence",
            "Player first",
            "Creativity",
            "Collaboration"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Unreal Engine, C++, graphics, game development",
                "common_topics": ["Unreal Engine", "C++", "Graphics programming", "Game optimization", "Rendering"],
                "style": "Extremely technical, graphics and engine focus",
                "tips": "Know Unreal Engine. Strong C++ required. Graphics programming. Game optimization."
            },
            "Behavioral": {
                "focus": "Innovation, excellence, creativity",
                "common_questions": [
                    "Why Epic? Experience with Unreal Engine?",
                    "Tell me about a graphics optimization project",
                    "Describe your game development experience",
                    "How do you approach performance?"
                ],
                "style": "Technical depth + creative passion"
            },
            "System Design": {
                "focus": "Game engine, graphics, real-time rendering",
                "common_topics": ["Design rendering pipeline", "Design game engine feature", "Design asset system"],
                "style": "Focus on performance and graphics quality"
            }
        },
        "red_flags": ["Weak C++", "No graphics knowledge", "Not performance-focused", "No gaming passion"],
        "average_process_duration": "6-8 weeks",
        "interview_count": "5-7 rounds"
    },
    
    # ========== CYBERSECURITY ==========
    "Palo Alto Networks": {
        "name": "Palo Alto Networks",
        "industry": "Cybersecurity",
        "size": "Large (>10000)",
        "interview_style": "security-focused",
        "difficulty_level": "High",
        "cultural_values": [
            "Disruption",
            "Execution",
            "Collaboration",
            "Integrity",
            "Inclusion"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Cybersecurity, networking, threat detection, firewalls",
                "common_topics": ["Network security", "Threat detection", "Firewalls", "Intrusion prevention", "Security protocols"],
                "style": "Security-first mindset, deep technical knowledge",
                "tips": "Know cybersecurity fundamentals. Discuss threat landscape. Network security expertise."
            },
            "Behavioral": {
                "focus": "Security mindset, collaboration, execution",
                "common_questions": [
                    "How do you approach security threats?",
                    "Tell me about a security incident you handled",
                    "Describe your security philosophy",
                    "How do you stay updated on threats?"
                ],
                "style": "Security-conscious, professional"
            },
            "System Design": {
                "focus": "Security systems, threat detection, network security",
                "common_topics": ["Design firewall", "Design threat detection system", "Design security monitoring"],
                "style": "Security-first approach to all designs"
            }
        },
        "red_flags": ["Weak security knowledge", "Not security-conscious", "Ignoring threat landscape"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "CrowdStrike": {
        "name": "CrowdStrike",
        "industry": "Cybersecurity/Endpoint Security",
        "size": "Medium (5000-10000)",
        "interview_style": "threat-intelligence-focused",
        "difficulty_level": "Very High",
        "cultural_values": [
            "Customer first",
            "Innovation",
            "Integrity",
            "Teamwork",
            "Excellence"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Endpoint security, threat intelligence, cloud-native, AI/ML",
                "common_topics": ["Endpoint detection", "Threat hunting", "Cloud security", "AI for security", "Incident response"],
                "style": "Advanced security, threat intelligence focus",
                "tips": "Know endpoint security. Discuss threat intelligence. Cloud-native security. AI/ML for security."
            },
            "Behavioral": {
                "focus": "Customer focus, innovation, threat mindset",
                "common_questions": [
                    "How do you approach threat detection?",
                    "Tell me about analyzing a security breach",
                    "Describe your incident response experience",
                    "How do you think about adversaries?"
                ],
                "style": "Threat-focused, customer-centric"
            },
            "System Design": {
                "focus": "Endpoint security, threat detection, cloud-native",
                "common_topics": ["Design EDR system", "Design threat intelligence platform", "Design incident response"],
                "style": "Focus on real-time threat detection and response"
            }
        },
        "red_flags": ["Weak security knowledge", "Not threat-aware", "Ignoring cloud security"],
        "average_process_duration": "6-8 weeks",
        "interview_count": "5-6 rounds"
    },
    
    # ========== CLOUD & INFRASTRUCTURE ==========
    "DigitalOcean": {
        "name": "DigitalOcean",
        "industry": "Cloud/Infrastructure",
        "size": "Medium (1000-5000)",
        "interview_style": "developer-experience-cloud",
        "difficulty_level": "High",
        "cultural_values": [
            "Simplicity",
            "Developer love",
            "Ownership",
            "Transparency",
            "Community"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Cloud infrastructure, developer experience, distributed systems",
                "common_topics": ["Kubernetes", "Cloud infrastructure", "Networking", "Storage", "Developer tools"],
                "style": "Developer-focused, simplicity emphasis",
                "tips": "Know cloud infrastructure. Discuss developer experience. Simplicity over complexity."
            },
            "Behavioral": {
                "focus": "Developer empathy, simplicity, ownership",
                "common_questions": [
                    "How would you improve DigitalOcean's developer experience?",
                    "Tell me about simplifying complex systems",
                    "Describe your cloud infrastructure experience",
                    "How do you approach developer tools?"
                ],
                "style": "Developer-focused, simplicity-driven"
            },
            "System Design": {
                "focus": "Cloud platform, developer tools, infrastructure",
                "common_topics": ["Design cloud platform", "Design managed database", "Design networking"],
                "style": "Focus on simplicity and developer experience"
            }
        },
        "red_flags": ["Overengineering", "Not developer-focused", "Weak cloud knowledge"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Cloudflare": {
        "name": "Cloudflare",
        "industry": "Cloud/CDN/Security",
        "size": "Medium (5000-10000)",
        "interview_style": "edge-computing-focused",
        "difficulty_level": "Very High",
        "cultural_values": [
            "Build a better Internet",
            "Transparency",
            "Empathy",
            "Curiosity",
            "Tenacity"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Edge computing, CDN, DDoS protection, networking, performance",
                "common_topics": ["Edge computing", "CDN", "DDoS mitigation", "Networking", "Performance optimization"],
                "style": "Deep technical, networking and performance focus",
                "tips": "Know edge computing and CDN. Discuss DDoS protection. Network protocols. Performance optimization."
            },
            "Behavioral": {
                "focus": "Mission alignment, curiosity, tenacity",
                "common_questions": [
                    "Why Cloudflare? Why build a better Internet?",
                    "Tell me about optimizing performance at scale",
                    "Describe your approach to DDoS protection",
                    "How do you think about edge computing?"
                ],
                "style": "Mission-driven, technically deep"
            },
            "System Design": {
                "focus": "Edge computing, CDN, DDoS protection, global scale",
                "common_topics": ["Design CDN", "Design DDoS mitigation", "Design edge computing platform"],
                "style": "Focus on global scale and performance"
            }
        },
        "red_flags": ["Weak networking knowledge", "Not performance-focused", "Ignoring security"],
        "average_process_duration": "6-8 weeks",
        "interview_count": "5-7 rounds"
    },
    
    # ========== MEDIA & ENTERTAINMENT ==========
    "Spotify": {
        "name": "Spotify",
        "industry": "Media/Music Streaming",
        "size": "Large (>5000)",
        "interview_style": "product-and-scale",
        "difficulty_level": "High",
        "cultural_values": [
            "Innovation",
            "Collaboration",
            "Sincerity",
            "Passion",
            "Playfulness"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Streaming, recommendation systems, mobile, backend scale",
                "common_topics": ["Music streaming", "Recommendation algorithms", "Mobile apps", "Backend systems", "Data pipelines"],
                "style": "Product-focused, emphasis on user experience and scale",
                "tips": "Know streaming technology. Discuss recommendation systems. Mobile experience. Data at scale."
            },
            "Behavioral": {
                "focus": "Innovation, collaboration, passion for music",
                "common_questions": [
                    "How would you improve Spotify?",
                    "Tell me about building recommendation systems",
                    "Describe your approach to streaming",
                    "What's your relationship with music?"
                ],
                "style": "Product-focused, music passion valued"
            },
            "System Design": {
                "focus": "Music streaming, recommendations, personalization",
                "common_topics": ["Design music streaming", "Design recommendation engine", "Design playlist system"],
                "style": "Focus on user experience and personalization"
            }
        },
        "red_flags": ["Not product-focused", "Weak recommendation knowledge", "No music passion"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "4-6 rounds"
    },
    
    "Discord": {
        "name": "Discord",
        "industry": "Communication/Social",
        "size": "Medium (500-1000)",
        "interview_style": "community-and-real-time",
        "difficulty_level": "High",
        "cultural_values": [
            "Community first",
            "Innovation",
            "Quality",
            "Transparency",
            "Inclusivity"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Real-time communication, voice/video, community features, scale",
                "common_topics": ["WebRTC", "Real-time messaging", "Voice chat", "Community moderation", "Mobile apps"],
                "style": "Real-time systems focus, community-oriented",
                "tips": "Know real-time communication. Discuss WebRTC. Community features. Low-latency systems."
            },
            "Behavioral": {
                "focus": "Community focus, innovation, quality",
                "common_questions": [
                    "How would you improve Discord?",
                    "Tell me about building real-time systems",
                    "Describe your approach to community features",
                    "How do you think about moderation?"
                ],
                "style": "Community-focused, quality-driven"
            },
            "System Design": {
                "focus": "Real-time communication, voice/video, community",
                "common_topics": ["Design voice chat", "Design messaging system", "Design community moderation"],
                "style": "Focus on real-time and community experience"
            }
        },
        "red_flags": ["Weak real-time knowledge", "Not community-focused", "Poor quality standards"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "4-5 rounds"
    },
    
    # ========== HEALTHCARE TECH ==========
    "Teladoc Health": {
        "name": "Teladoc Health",
        "industry": "Healthcare/Telemedicine",
        "size": "Large (>5000)",
        "interview_style": "healthcare-and-compliance",
        "difficulty_level": "Medium-High",
        "cultural_values": [
            "Patient first",
            "Innovation",
            "Integrity",
            "Collaboration",
            "Excellence"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Telemedicine, HIPAA compliance, video conferencing, healthcare systems",
                "common_topics": ["Telemedicine platforms", "HIPAA compliance", "Video conferencing", "EHR integration", "Security"],
                "style": "Healthcare-focused, compliance-heavy",
                "tips": "Understand HIPAA. Discuss healthcare workflows. Security and privacy critical. Patient experience."
            },
            "Behavioral": {
                "focus": "Patient focus, compliance, integrity",
                "common_questions": [
                    "How do you ensure HIPAA compliance?",
                    "Tell me about building healthcare systems",
                    "Describe your approach to patient privacy",
                    "How do you handle sensitive data?"
                ],
                "style": "Patient-focused, compliance-conscious"
            },
            "System Design": {
                "focus": "Telemedicine platform, compliance, security",
                "common_topics": ["Design telemedicine platform", "Design EHR integration", "Design secure video"],
                "style": "Focus on compliance and patient safety"
            }
        },
        "red_flags": ["Ignoring compliance", "Weak security", "Not patient-focused"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "4-5 rounds"
    },
    
    # ========== TRAVEL & HOSPITALITY ==========
    "Booking.com": {
        "name": "Booking.com",
        "industry": "Travel/E-commerce",
        "size": "Large (>10000)",
        "interview_style": "data-driven-and-experimentation",
        "difficulty_level": "High",
        "cultural_values": [
            "Customer first",
            "Data-driven",
            "Experimentation",
            "Ownership",
            "Collaboration"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "E-commerce, A/B testing, data-driven, search, recommendations",
                "common_topics": ["A/B testing", "Search algorithms", "Recommendation systems", "Data pipelines", "Experimentation"],
                "style": "Data-driven, experimentation culture",
                "tips": "Know A/B testing deeply. Discuss experimentation. Data-driven decision making. Search and recommendations."
            },
            "Behavioral": {
                "focus": "Customer focus, data-driven, experimentation",
                "common_questions": [
                    "How would you improve booking conversion?",
                    "Tell me about an A/B test you ran",
                    "Describe your approach to experimentation",
                    "How do you make data-driven decisions?"
                ],
                "style": "Data-focused, experimentation-driven"
            },
            "System Design": {
                "focus": "Travel platform, search, recommendations, experimentation",
                "common_topics": ["Design hotel search", "Design recommendation engine", "Design A/B testing platform"],
                "style": "Focus on data-driven optimization"
            }
        },
        "red_flags": ["Not data-driven", "Weak experimentation knowledge", "Ignoring metrics"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "5-6 rounds"
    }
}

# ============================================
# BATCH ADD FUNCTION
# ============================================

def batch_add_companies():
    """Add all domain-expansion companies to the database"""
    
    # Load existing data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'data', 'company_profiles.json')
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("="*60)
    print("BATCH ADDING COMPANIES - ROUND 4 (DOMAIN EXPANSION)")
    print("="*60)
    print(f"\nCompanies to add: {len(COMPANIES_TO_ADD)}")
    print("\nDomains covered:")
    print("  - E-commerce & Retail (Shopee, Instacart)")
    print("  - Gaming (Riot Games, Epic Games)")
    print("  - Cybersecurity (Palo Alto Networks, CrowdStrike)")
    print("  - Cloud & Infrastructure (DigitalOcean, Cloudflare)")
    print("  - Media & Entertainment (Spotify, Discord)")
    print("  - Healthcare Tech (Teladoc Health)")
    print("  - Travel (Booking.com)")
    
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
    data['meta']['version'] = "4.0.0"
    
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
