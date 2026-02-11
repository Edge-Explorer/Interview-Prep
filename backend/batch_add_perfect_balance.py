"""
Batch script to achieve PERFECT BALANCE - Round 6
Goal: Get each domain to 10+ companies
Focus: Gaming, Cybersecurity, Healthcare, Travel, Media, Food Delivery + more
"""

import json
import os

# ============================================
# COMPANIES TO ADD - ROUND 6 (PERFECT BALANCE)
# ============================================

COMPANIES_TO_ADD = {
    # ========== MORE GAMING (Target: 10+) ==========
    "Activision Blizzard": {
        "name": "Activision Blizzard",
        "industry": "Gaming/Entertainment",
        "size": "Large (>10000)",
        "interview_style": "aaa-game-development",
        "difficulty_level": "High",
        "cultural_values": ["Player first", "Innovation", "Excellence", "Collaboration", "Passion"],
        "interview_rounds": {
            "Technical": {
                "focus": "AAA game development, C++, game engines, multiplayer",
                "common_topics": ["C++", "Game engines", "Multiplayer networking", "Game optimization", "Graphics"],
                "style": "AAA game focus, technical excellence",
                "tips": "Know AAA game development. Strong C++. Discuss multiplayer systems. Game optimization."
            },
            "Behavioral": {
                "focus": "Player focus, passion for gaming, collaboration",
                "common_questions": ["Why Blizzard?", "Favorite Blizzard game?", "Tell me about game development", "How do you ensure quality?"],
                "style": "Gaming passion valued, quality-focused"
            },
            "System Design": {
                "focus": "Game systems, multiplayer, matchmaking",
                "common_topics": ["Design matchmaking", "Design game server", "Design anti-cheat"],
                "style": "Focus on player experience and quality"
            }
        },
        "red_flags": ["Not a gamer", "Weak C++", "No AAA experience"],
        "average_process_duration": "6-8 weeks",
        "interview_count": "5-6 rounds"
    },
    
    "Valve": {
        "name": "Valve",
        "industry": "Gaming/Platform",
        "size": "Medium (500-1000)",
        "interview_style": "flat-structure-excellence",
        "difficulty_level": "Very High",
        "cultural_values": ["Flat hierarchy", "Innovation", "Excellence", "Player focus", "Autonomy"],
        "interview_rounds": {
            "Technical": {
                "focus": "Game development, Steam platform, C++, distributed systems",
                "common_topics": ["C++", "Game engines", "Platform engineering", "Distributed systems", "VR"],
                "style": "Extremely high bar, flat structure, self-directed",
                "tips": "Extremely selective. Show initiative. Strong technical skills. Gaming passion critical."
            },
            "Behavioral": {
                "focus": "Self-direction, innovation, flat hierarchy fit",
                "common_questions": ["How do you work without managers?", "Tell me about self-directed projects", "Why Valve?", "How do you prioritize?"],
                "style": "Unique culture, autonomy-focused"
            },
            "System Design": {
                "focus": "Steam platform, game systems, VR",
                "common_topics": ["Design game distribution", "Design VR system", "Design multiplayer"],
                "style": "Innovation and excellence focus"
            }
        },
        "red_flags": ["Needs direction", "Not self-motivated", "Weak gaming passion"],
        "average_process_duration": "8-12 weeks",
        "interview_count": "6-8 rounds"
    },
    
    "EA (Electronic Arts)": {
        "name": "EA (Electronic Arts)",
        "industry": "Gaming/Sports Games",
        "size": "Large (>10000)",
        "interview_style": "sports-and-live-services",
        "difficulty_level": "Medium-High",
        "cultural_values": ["Player first", "Innovation", "Inclusion", "Integrity", "Quality"],
        "interview_rounds": {
            "Technical": {
                "focus": "Game development, live services, sports games, mobile",
                "common_topics": ["Game engines", "Live services", "Mobile games", "Sports simulation", "Multiplayer"],
                "style": "Live services focus, sports games expertise",
                "tips": "Know live services. Discuss sports games. Mobile gaming. Player engagement."
            },
            "Behavioral": {
                "focus": "Player focus, innovation, inclusion",
                "common_questions": ["Why EA?", "How would you improve FIFA/Madden?", "Tell me about live services", "How do you engage players?"],
                "style": "Player-focused, live services mindset"
            },
            "System Design": {
                "focus": "Live services, sports games, player engagement",
                "common_topics": ["Design live service", "Design sports game", "Design player progression"],
                "style": "Focus on engagement and monetization"
            }
        },
        "red_flags": ["No live services knowledge", "Not player-focused", "Weak gaming passion"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Ubisoft": {
        "name": "Ubisoft",
        "industry": "Gaming/AAA Games",
        "size": "Large (>15000)",
        "interview_style": "creative-and-technical",
        "difficulty_level": "Medium-High",
        "cultural_values": ["Creativity", "Innovation", "Player focus", "Collaboration", "Diversity"],
        "interview_rounds": {
            "Technical": {
                "focus": "Game development, open world, C++, game engines",
                "common_topics": ["C++", "Game engines", "Open world systems", "AI", "Graphics"],
                "style": "Creative + technical, open world focus",
                "tips": "Know open world development. Discuss game AI. Creative problem-solving."
            },
            "Behavioral": {
                "focus": "Creativity, collaboration, diversity",
                "common_questions": ["Why Ubisoft?", "Tell me about creative projects", "How do you collaborate?", "Describe your game development experience"],
                "style": "Creative, collaborative, diverse"
            },
            "System Design": {
                "focus": "Open world games, AI systems, multiplayer",
                "common_topics": ["Design open world", "Design game AI", "Design multiplayer"],
                "style": "Focus on creativity and player experience"
            }
        },
        "red_flags": ["Not creative", "Weak collaboration", "No AAA experience"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Supercell": {
        "name": "Supercell",
        "industry": "Gaming/Mobile Games",
        "size": "Small (<500)",
        "interview_style": "small-teams-big-impact",
        "difficulty_level": "Very High",
        "cultural_values": ["Small teams", "Player first", "Innovation", "Autonomy", "Quality"],
        "interview_rounds": {
            "Technical": {
                "focus": "Mobile games, live ops, player engagement, small teams",
                "common_topics": ["Mobile gaming", "Live operations", "Player retention", "Game balance", "Analytics"],
                "style": "Mobile-first, small team mindset, high autonomy",
                "tips": "Know mobile gaming deeply. Discuss live ops. Player retention. Small team experience."
            },
            "Behavioral": {
                "focus": "Small team fit, player focus, autonomy",
                "common_questions": ["Why Supercell?", "How do you work in small teams?", "Tell me about mobile games", "How do you ensure quality?"],
                "style": "Small team culture, high autonomy"
            },
            "System Design": {
                "focus": "Mobile games, live ops, player engagement",
                "common_topics": ["Design mobile game", "Design live ops", "Design player progression"],
                "style": "Focus on player retention and monetization"
            }
        },
        "red_flags": ["Needs large team", "Not mobile-focused", "Weak live ops knowledge"],
        "average_process_duration": "6-8 weeks",
        "interview_count": "5-6 rounds"
    },
    
    "Krafton": {
        "name": "Krafton",
        "industry": "Gaming/Battle Royale",
        "size": "Medium (1000-5000)",
        "interview_style": "battle-royale-focused",
        "difficulty_level": "High",
        "cultural_values": ["Innovation", "Player focus", "Excellence", "Creativity", "Global mindset"],
        "interview_rounds": {
            "Technical": {
                "focus": "Battle royale, multiplayer, Unreal Engine, mobile",
                "common_topics": ["Unreal Engine", "Multiplayer networking", "Battle royale systems", "Mobile optimization", "Anti-cheat"],
                "style": "Battle royale expertise, multiplayer focus",
                "tips": "Know PUBG/battle royale. Discuss multiplayer networking. Anti-cheat. Mobile optimization."
            },
            "Behavioral": {
                "focus": "Innovation, player focus, global mindset",
                "common_questions": ["Why Krafton?", "How would you improve PUBG?", "Tell me about multiplayer systems", "How do you think globally?"],
                "style": "Player-focused, global perspective"
            },
            "System Design": {
                "focus": "Battle royale, multiplayer, anti-cheat",
                "common_topics": ["Design battle royale", "Design anti-cheat", "Design matchmaking"],
                "style": "Focus on competitive gaming and fairness"
            }
        },
        "red_flags": ["Weak multiplayer knowledge", "Not player-focused", "No battle royale experience"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "4-5 rounds"
    },
    
    # ========== MORE CYBERSECURITY (Target: 10+) ==========
    "Fortinet": {
        "name": "Fortinet",
        "industry": "Cybersecurity/Network Security",
        "size": "Large (>10000)",
        "interview_style": "network-security-focused",
        "difficulty_level": "High",
        "cultural_values": ["Customer focus", "Innovation", "Integrity", "Collaboration", "Excellence"],
        "interview_rounds": {
            "Technical": {
                "focus": "Network security, firewalls, threat detection, SD-WAN",
                "common_topics": ["Firewalls", "Network security", "Threat detection", "SD-WAN", "Security protocols"],
                "style": "Network security expertise, technical depth",
                "tips": "Know network security deeply. Discuss firewalls. Threat landscape. SD-WAN."
            },
            "Behavioral": {
                "focus": "Customer focus, integrity, collaboration",
                "common_questions": ["How do you approach network security?", "Tell me about threat detection", "Describe security incident", "How do you help customers?"],
                "style": "Customer-focused, security-conscious"
            },
            "System Design": {
                "focus": "Network security, firewalls, threat detection",
                "common_topics": ["Design firewall", "Design threat detection", "Design SD-WAN"],
                "style": "Focus on network security and performance"
            }
        },
        "red_flags": ["Weak network security", "Not customer-focused", "Ignoring threats"],
        "average_process_duration": "5-6 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Check Point": {
        "name": "Check Point",
        "industry": "Cybersecurity/Network Security",
        "size": "Medium (5000-10000)",
        "interview_style": "security-research-focused",
        "difficulty_level": "High",
        "cultural_values": ["Innovation", "Excellence", "Customer success", "Integrity", "Teamwork"],
        "interview_rounds": {
            "Technical": {
                "focus": "Cybersecurity, threat research, firewalls, cloud security",
                "common_topics": ["Threat research", "Firewalls", "Cloud security", "Malware analysis", "Network security"],
                "style": "Research-oriented, deep security knowledge",
                "tips": "Know threat research. Discuss malware analysis. Cloud security. Network protocols."
            },
            "Behavioral": {
                "focus": "Innovation, customer success, integrity",
                "common_questions": ["How do you research threats?", "Tell me about security research", "Describe threat analysis", "How do you innovate?"],
                "style": "Research-focused, innovation-driven"
            },
            "System Design": {
                "focus": "Security systems, threat detection, cloud security",
                "common_topics": ["Design threat detection", "Design cloud security", "Design firewall"],
                "style": "Focus on threat prevention and research"
            }
        },
        "red_flags": ["Weak research skills", "Not innovative", "Ignoring cloud security"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Splunk": {
        "name": "Splunk",
        "industry": "Cybersecurity/SIEM",
        "size": "Medium (5000-10000)",
        "interview_style": "data-and-security",
        "difficulty_level": "High",
        "cultural_values": ["Innovation", "Customer success", "Passion", "Integrity", "Collaboration"],
        "interview_rounds": {
            "Technical": {
                "focus": "SIEM, log analysis, security analytics, big data",
                "common_topics": ["SIEM", "Log analysis", "Security analytics", "Big data", "Machine learning"],
                "style": "Data-driven security, analytics focus",
                "tips": "Know SIEM systems. Discuss log analysis. Security analytics. Big data processing."
            },
            "Behavioral": {
                "focus": "Innovation, customer success, passion",
                "common_questions": ["How do you analyze security data?", "Tell me about SIEM", "Describe threat hunting", "How do you help customers?"],
                "style": "Data-focused, customer-centric"
            },
            "System Design": {
                "focus": "SIEM, log processing, security analytics",
                "common_topics": ["Design SIEM", "Design log processing", "Design threat detection"],
                "style": "Focus on data processing and analytics"
            }
        },
        "red_flags": ["Weak data skills", "Not analytical", "Ignoring security"],
        "average_process_duration": "5-6 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Rapid7": {
        "name": "Rapid7",
        "industry": "Cybersecurity/Vulnerability Management",
        "size": "Medium (1000-5000)",
        "interview_style": "vulnerability-focused",
        "difficulty_level": "High",
        "cultural_values": ["Customer focus", "Innovation", "Collaboration", "Integrity", "Excellence"],
        "interview_rounds": {
            "Technical": {
                "focus": "Vulnerability management, penetration testing, security research",
                "common_topics": ["Vulnerability scanning", "Penetration testing", "Metasploit", "Security research", "Threat intelligence"],
                "style": "Offensive security focus, research-oriented",
                "tips": "Know vulnerability management. Discuss pen testing. Metasploit. Security research."
            },
            "Behavioral": {
                "focus": "Customer focus, innovation, collaboration",
                "common_questions": ["How do you find vulnerabilities?", "Tell me about pen testing", "Describe security research", "How do you help customers?"],
                "style": "Research-focused, customer-centric"
            },
            "System Design": {
                "focus": "Vulnerability management, scanning, threat intelligence",
                "common_topics": ["Design vulnerability scanner", "Design pen testing platform", "Design threat intelligence"],
                "style": "Focus on offensive security and research"
            }
        },
        "red_flags": ["Weak offensive security", "Not research-oriented", "Ignoring vulnerabilities"],
        "average_process_duration": "5-6 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Darktrace": {
        "name": "Darktrace",
        "industry": "Cybersecurity/AI Security",
        "size": "Medium (1000-5000)",
        "interview_style": "ai-security-focused",
        "difficulty_level": "Very High",
        "cultural_values": ["Innovation", "Excellence", "Customer success", "Collaboration", "Integrity"],
        "interview_rounds": {
            "Technical": {
                "focus": "AI for security, anomaly detection, machine learning, threat hunting",
                "common_topics": ["Machine learning", "Anomaly detection", "Threat hunting", "Network security", "AI"],
                "style": "AI/ML focus, cutting-edge security",
                "tips": "Know ML for security. Discuss anomaly detection. Threat hunting. AI systems."
            },
            "Behavioral": {
                "focus": "Innovation, excellence, customer success",
                "common_questions": ["How do you use AI for security?", "Tell me about anomaly detection", "Describe ML projects", "How do you innovate?"],
                "style": "Innovation-focused, AI-driven"
            },
            "System Design": {
                "focus": "AI security, anomaly detection, threat hunting",
                "common_topics": ["Design AI security system", "Design anomaly detection", "Design threat hunting"],
                "style": "Focus on AI/ML and innovation"
            }
        },
        "red_flags": ["Weak ML knowledge", "Not innovative", "Ignoring AI"],
        "average_process_duration": "6-8 weeks",
        "interview_count": "5-6 rounds"
    },
    
    "Tanium": {
        "name": "Tanium",
        "industry": "Cybersecurity/Endpoint Management",
        "size": "Medium (1000-5000)",
        "interview_style": "endpoint-security-focused",
        "difficulty_level": "High",
        "cultural_values": ["Customer obsession", "Innovation", "Integrity", "Collaboration", "Excellence"],
        "interview_rounds": {
            "Technical": {
                "focus": "Endpoint management, security, real-time visibility, scale",
                "common_topics": ["Endpoint security", "Real-time systems", "Distributed systems", "Security monitoring", "Scale"],
                "style": "Endpoint focus, real-time systems",
                "tips": "Know endpoint security. Discuss real-time visibility. Distributed systems. Scale."
            },
            "Behavioral": {
                "focus": "Customer obsession, innovation, integrity",
                "common_questions": ["How do you secure endpoints?", "Tell me about real-time systems", "Describe distributed systems", "How do you help customers?"],
                "style": "Customer-focused, technical depth"
            },
            "System Design": {
                "focus": "Endpoint management, real-time visibility, scale",
                "common_topics": ["Design endpoint management", "Design real-time monitoring", "Design distributed system"],
                "style": "Focus on real-time and scale"
            }
        },
        "red_flags": ["Weak endpoint knowledge", "Not customer-focused", "Ignoring scale"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "4-5 rounds"
    },
    
    # ========== MORE HEALTHCARE (Target: 10+) ==========
    "Philips Healthcare": {
        "name": "Philips Healthcare",
        "industry": "Healthcare/Medical Devices",
        "size": "Large (>70000)",
        "interview_style": "medical-devices-focused",
        "difficulty_level": "Medium-High",
        "cultural_values": ["Patient focus", "Innovation", "Quality", "Integrity", "Collaboration"],
        "interview_rounds": {
            "Technical": {
                "focus": "Medical devices, embedded systems, imaging, healthcare IT",
                "common_topics": ["Embedded systems", "Medical imaging", "Healthcare IT", "Regulatory compliance", "Quality"],
                "style": "Medical device focus, regulatory-heavy",
                "tips": "Know medical devices. Discuss regulatory compliance. Embedded systems. Quality critical."
            },
            "Behavioral": {
                "focus": "Patient focus, quality, integrity",
                "common_questions": ["Why healthcare?", "Tell me about medical devices", "Describe quality approach", "How do you ensure safety?"],
                "style": "Patient-focused, quality-driven"
            },
            "System Design": {
                "focus": "Medical devices, imaging, healthcare IT",
                "common_topics": ["Design medical device", "Design imaging system", "Design healthcare IT"],
                "style": "Focus on safety and regulatory compliance"
            }
        },
        "red_flags": ["Not quality-focused", "Ignoring compliance", "Weak embedded systems"],
        "average_process_duration": "6-8 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Medtronic": {
        "name": "Medtronic",
        "industry": "Healthcare/Medical Devices",
        "size": "Large (>90000)",
        "interview_style": "medical-technology-focused",
        "difficulty_level": "Medium-High",
        "cultural_values": ["Patient first", "Innovation", "Inclusion", "Integrity", "Collaboration"],
        "interview_rounds": {
            "Technical": {
                "focus": "Medical devices, embedded systems, IoT, regulatory",
                "common_topics": ["Embedded systems", "Medical devices", "IoT", "Regulatory", "Quality"],
                "style": "Medical technology focus, regulatory compliance",
                "tips": "Know medical devices. Discuss embedded systems. IoT. Regulatory compliance."
            },
            "Behavioral": {
                "focus": "Patient focus, innovation, integrity",
                "common_questions": ["Why Medtronic?", "Tell me about medical technology", "Describe quality approach", "How do you innovate?"],
                "style": "Patient-focused, mission-driven"
            },
            "System Design": {
                "focus": "Medical devices, IoT, connectivity",
                "common_topics": ["Design medical device", "Design IoT system", "Design connectivity"],
                "style": "Focus on patient safety and quality"
            }
        },
        "red_flags": ["Not patient-focused", "Ignoring compliance", "Weak quality mindset"],
        "average_process_duration": "6-8 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "GE Healthcare": {
        "name": "GE Healthcare",
        "industry": "Healthcare/Medical Technology",
        "size": "Large (>50000)",
        "interview_style": "industrial-healthcare",
        "difficulty_level": "Medium-High",
        "cultural_values": ["Patient focus", "Innovation", "Quality", "Integrity", "Inclusion"],
        "interview_rounds": {
            "Technical": {
                "focus": "Medical imaging, diagnostics, healthcare IT, AI",
                "common_topics": ["Medical imaging", "Diagnostics", "Healthcare IT", "AI/ML", "Quality"],
                "style": "Industrial + healthcare, innovation focus",
                "tips": "Know medical imaging. Discuss diagnostics. AI in healthcare. Quality systems."
            },
            "Behavioral": {
                "focus": "Patient focus, innovation, quality",
                "common_questions": ["Why GE Healthcare?", "Tell me about medical imaging", "Describe innovation", "How do you ensure quality?"],
                "style": "Patient-focused, innovation-driven"
            },
            "System Design": {
                "focus": "Medical imaging, diagnostics, AI",
                "common_topics": ["Design imaging system", "Design diagnostic tool", "Design AI for healthcare"],
                "style": "Focus on innovation and quality"
            }
        },
        "red_flags": ["Not innovative", "Ignoring quality", "Weak healthcare knowledge"],
        "average_process_duration": "6-8 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Siemens Healthineers": {
        "name": "Siemens Healthineers",
        "industry": "Healthcare/Medical Technology",
        "size": "Large (>65000)",
        "interview_style": "precision-medicine-focused",
        "difficulty_level": "Medium-High",
        "cultural_values": ["Patient focus", "Innovation", "Excellence", "Integrity", "Collaboration"],
        "interview_rounds": {
            "Technical": {
                "focus": "Medical imaging, diagnostics, precision medicine, AI",
                "common_topics": ["Medical imaging", "Precision medicine", "Diagnostics", "AI", "Quality"],
                "style": "Precision medicine focus, technical excellence",
                "tips": "Know precision medicine. Discuss medical imaging. AI in diagnostics. Quality."
            },
            "Behavioral": {
                "focus": "Patient focus, innovation, excellence",
                "common_questions": ["Why Siemens Healthineers?", "Tell me about precision medicine", "Describe innovation", "How do you ensure quality?"],
                "style": "Patient-focused, excellence-driven"
            },
            "System Design": {
                "focus": "Precision medicine, imaging, diagnostics",
                "common_topics": ["Design imaging system", "Design diagnostic platform", "Design precision medicine"],
                "style": "Focus on precision and quality"
            }
        },
        "red_flags": ["Not patient-focused", "Ignoring quality", "Weak technical skills"],
        "average_process_duration": "6-8 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Athenahealth": {
        "name": "Athenahealth",
        "industry": "Healthcare/Health IT",
        "size": "Medium (5000-10000)",
        "interview_style": "cloud-healthcare-focused",
        "difficulty_level": "Medium",
        "cultural_values": ["Customer success", "Innovation", "Integrity", "Collaboration", "Excellence"],
        "interview_rounds": {
            "Technical": {
                "focus": "Cloud healthcare, EHR, practice management, interoperability",
                "common_topics": ["Cloud systems", "EHR", "Practice management", "Interoperability", "Healthcare workflows"],
                "style": "Cloud-based healthcare, customer focus",
                "tips": "Know cloud healthcare. Discuss EHR. Interoperability. Customer success."
            },
            "Behavioral": {
                "focus": "Customer success, innovation, collaboration",
                "common_questions": ["How do you help healthcare providers?", "Tell me about cloud healthcare", "Describe interoperability", "How do you innovate?"],
                "style": "Customer-focused, cloud-native"
            },
            "System Design": {
                "focus": "Cloud EHR, practice management, interoperability",
                "common_topics": ["Design cloud EHR", "Design practice management", "Design interoperability"],
                "style": "Focus on cloud and customer success"
            }
        },
        "red_flags": ["Not customer-focused", "Weak cloud knowledge", "Ignoring healthcare"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "4 rounds"
    },
    
    "Zocdoc": {
        "name": "Zocdoc",
        "industry": "Healthcare/Marketplace",
        "size": "Small (500-1000)",
        "interview_style": "healthcare-marketplace",
        "difficulty_level": "Medium",
        "cultural_values": ["Patient focus", "Innovation", "Transparency", "Collaboration", "Excellence"],
        "interview_rounds": {
            "Technical": {
                "focus": "Healthcare marketplace, scheduling, search, mobile",
                "common_topics": ["Marketplace", "Scheduling systems", "Search", "Mobile apps", "Healthcare"],
                "style": "Marketplace focus, patient experience",
                "tips": "Understand healthcare marketplace. Discuss scheduling. Search algorithms. Patient experience."
            },
            "Behavioral": {
                "focus": "Patient focus, innovation, transparency",
                "common_questions": ["How would you improve Zocdoc?", "Tell me about healthcare marketplace", "Describe patient experience", "How do you innovate?"],
                "style": "Patient-focused, marketplace-oriented"
            },
            "System Design": {
                "focus": "Healthcare marketplace, scheduling, search",
                "common_topics": ["Design marketplace", "Design scheduling", "Design search"],
                "style": "Focus on patient experience and marketplace"
            }
        },
        "red_flags": ["Not patient-focused", "Weak marketplace knowledge", "Ignoring healthcare"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "4 rounds"
    },
    
    "1mg (Tata 1mg)": {
        "name": "1mg (Tata 1mg)",
        "industry": "Healthcare/E-Pharmacy",
        "size": "Medium (1000-5000)",
        "interview_style": "healthtech-india-focused",
        "difficulty_level": "Medium",
        "cultural_values": ["Patient first", "Innovation", "Trust", "Accessibility", "Excellence"],
        "interview_rounds": {
            "Technical": {
                "focus": "E-pharmacy, healthcare marketplace, mobile, logistics",
                "common_topics": ["E-commerce", "Healthcare", "Mobile apps", "Logistics", "Telemedicine"],
                "style": "Indian healthtech, mobile-first",
                "tips": "Know Indian healthcare. Discuss e-pharmacy. Mobile experience. Logistics."
            },
            "Behavioral": {
                "focus": "Patient focus, trust, accessibility",
                "common_questions": ["How do you ensure medicine authenticity?", "Tell me about healthcare accessibility", "Describe patient trust", "How do you innovate?"],
                "style": "Patient-focused, trust-driven"
            },
            "System Design": {
                "focus": "E-pharmacy, logistics, telemedicine",
                "common_topics": ["Design e-pharmacy", "Design logistics", "Design telemedicine"],
                "style": "Focus on trust and accessibility"
            }
        },
        "red_flags": ["Not patient-focused", "Ignoring trust", "Weak healthcare knowledge"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "3-4 rounds"
    },
    
    # ========== MORE TRAVEL (Target: 10+) ==========
    "Tripadvisor": {
        "name": "Tripadvisor",
        "industry": "Travel/Reviews",
        "size": "Medium (3000-5000)",
        "interview_style": "ugc-and-travel",
        "difficulty_level": "Medium-High",
        "cultural_values": ["Traveler first", "Innovation", "Trust", "Collaboration", "Excellence"],
        "interview_rounds": {
            "Technical": {
                "focus": "UGC, reviews, search, recommendations, travel",
                "common_topics": ["UGC systems", "Review moderation", "Search", "Recommendations", "Travel"],
                "style": "UGC focus, trust and quality",
                "tips": "Know UGC systems. Discuss review moderation. Search and recommendations. Trust."
            },
            "Behavioral": {
                "focus": "Traveler focus, trust, innovation",
                "common_questions": ["How do you ensure review quality?", "Tell me about UGC moderation", "Describe trust systems", "How do you help travelers?"],
                "style": "Traveler-focused, trust-driven"
            },
            "System Design": {
                "focus": "UGC, reviews, search, recommendations",
                "common_topics": ["Design review system", "Design UGC moderation", "Design search"],
                "style": "Focus on trust and quality"
            }
        },
        "red_flags": ["Ignoring trust", "Weak UGC knowledge", "Not traveler-focused"],
        "average_process_duration": "5-6 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Kayak": {
        "name": "Kayak",
        "industry": "Travel/Metasearch",
        "size": "Small (500-1000)",
        "interview_style": "metasearch-focused",
        "difficulty_level": "High",
        "cultural_values": ["Innovation", "Customer focus", "Excellence", "Collaboration", "Agility"],
        "interview_rounds": {
            "Technical": {
                "focus": "Metasearch, aggregation, search, pricing, mobile",
                "common_topics": ["Metasearch", "Data aggregation", "Search algorithms", "Pricing", "Mobile"],
                "style": "Metasearch focus, technical depth",
                "tips": "Know metasearch systems. Discuss data aggregation. Search algorithms. Pricing."
            },
            "Behavioral": {
                "focus": "Innovation, customer focus, agility",
                "common_questions": ["How would you improve Kayak?", "Tell me about metasearch", "Describe data aggregation", "How do you innovate?"],
                "style": "Innovation-focused, customer-centric"
            },
            "System Design": {
                "focus": "Metasearch, aggregation, search",
                "common_topics": ["Design metasearch", "Design aggregation", "Design search"],
                "style": "Focus on aggregation and search"
            }
        },
        "red_flags": ["Weak search knowledge", "Not innovative", "Ignoring customer"],
        "average_process_duration": "5-6 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "MakeMyTrip": {
        "name": "MakeMyTrip",
        "industry": "Travel/OTA",
        "size": "Medium (5000-10000)",
        "interview_style": "india-travel-focused",
        "difficulty_level": "Medium",
        "cultural_values": ["Customer first", "Innovation", "Integrity", "Collaboration", "Excellence"],
        "interview_rounds": {
            "Technical": {
                "focus": "Travel platform, booking, payments, mobile, India",
                "common_topics": ["Travel booking", "Payment systems", "Mobile apps", "Search", "India market"],
                "style": "Indian travel focus, mobile-first",
                "tips": "Know Indian travel market. Discuss booking systems. Mobile experience. Payments."
            },
            "Behavioral": {
                "focus": "Customer focus, innovation, integrity",
                "common_questions": ["How would you improve MakeMyTrip?", "Tell me about Indian travel", "Describe booking systems", "How do you innovate?"],
                "style": "Customer-focused, India-oriented"
            },
            "System Design": {
                "focus": "Travel booking, payments, search",
                "common_topics": ["Design booking system", "Design payment gateway", "Design search"],
                "style": "Focus on Indian market and mobile"
            }
        },
        "red_flags": ["Not customer-focused", "Weak travel knowledge", "Ignoring India market"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "3-4 rounds"
    },
    
    "Hopper": {
        "name": "Hopper",
        "industry": "Travel/Price Prediction",
        "size": "Small (500-1000)",
        "interview_style": "ai-and-mobile-travel",
        "difficulty_level": "High",
        "cultural_values": ["Innovation", "Customer obsession", "Data-driven", "Excellence", "Agility"],
        "interview_rounds": {
            "Technical": {
                "focus": "Price prediction, ML, mobile-first, travel",
                "common_topics": ["Machine learning", "Price prediction", "Mobile apps", "Data science", "Travel"],
                "style": "AI/ML focus, mobile-first, data-driven",
                "tips": "Know ML for pricing. Discuss price prediction. Mobile experience. Data science."
            },
            "Behavioral": {
                "focus": "Innovation, customer obsession, data-driven",
                "common_questions": ["How do you predict prices?", "Tell me about ML projects", "Describe mobile-first approach", "How do you innovate?"],
                "style": "Innovation-focused, data-driven"
            },
            "System Design": {
                "focus": "Price prediction, ML, mobile",
                "common_topics": ["Design price prediction", "Design ML system", "Design mobile app"],
                "style": "Focus on AI/ML and mobile"
            }
        },
        "red_flags": ["Weak ML knowledge", "Not mobile-first", "Ignoring data"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Skyscanner": {
        "name": "Skyscanner",
        "industry": "Travel/Metasearch",
        "size": "Medium (1000-3000)",
        "interview_style": "global-travel-search",
        "difficulty_level": "High",
        "cultural_values": ["Traveler first", "Innovation", "Collaboration", "Excellence", "Global mindset"],
        "interview_rounds": {
            "Technical": {
                "focus": "Travel search, metasearch, global scale, mobile",
                "common_topics": ["Search algorithms", "Metasearch", "Global scale", "Mobile apps", "Travel"],
                "style": "Global travel focus, search expertise",
                "tips": "Know travel search. Discuss metasearch. Global scale. Mobile experience."
            },
            "Behavioral": {
                "focus": "Traveler focus, innovation, global mindset",
                "common_questions": ["How would you improve Skyscanner?", "Tell me about travel search", "Describe global challenges", "How do you innovate?"],
                "style": "Traveler-focused, global perspective"
            },
            "System Design": {
                "focus": "Travel search, metasearch, global scale",
                "common_topics": ["Design travel search", "Design metasearch", "Design global platform"],
                "style": "Focus on search and global scale"
            }
        },
        "red_flags": ["Weak search knowledge", "Not global-minded", "Ignoring traveler"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Ctrip (Trip.com)": {
        "name": "Ctrip (Trip.com)",
        "industry": "Travel/OTA",
        "size": "Large (>30000)",
        "interview_style": "asia-travel-focused",
        "difficulty_level": "Medium-High",
        "cultural_values": ["Customer first", "Innovation", "Excellence", "Global mindset", "Collaboration"],
        "interview_rounds": {
            "Technical": {
                "focus": "Travel platform, booking, global scale, mobile, Asia",
                "common_topics": ["Travel booking", "Global scale", "Mobile apps", "Search", "Asia market"],
                "style": "Asia travel focus, global scale",
                "tips": "Know Asia travel market. Discuss global scale. Mobile experience. Booking systems."
            },
            "Behavioral": {
                "focus": "Customer focus, innovation, global mindset",
                "common_questions": ["How do you serve global travelers?", "Tell me about Asia travel", "Describe booking systems", "How do you innovate?"],
                "style": "Customer-focused, global perspective"
            },
            "System Design": {
                "focus": "Travel booking, global scale, mobile",
                "common_topics": ["Design booking system", "Design global platform", "Design mobile app"],
                "style": "Focus on global scale and Asia market"
            }
        },
        "red_flags": ["Not customer-focused", "Weak global knowledge", "Ignoring Asia market"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "4-5 rounds"
    },
    
    # ========== MORE MEDIA/ENTERTAINMENT (Target: 10+) ==========
    "YouTube": {
        "name": "YouTube",
        "industry": "Media/Video Platform",
        "size": "Large (part of Google)",
        "interview_style": "video-platform-scale",
        "difficulty_level": "Very High",
        "cultural_values": ["Creator focus", "Innovation", "Openness", "Excellence", "Global impact"],
        "interview_rounds": {
            "Technical": {
                "focus": "Video platform, recommendations, CDN, global scale, ML",
                "common_topics": ["Video processing", "Recommendation systems", "CDN", "Global scale", "ML"],
                "style": "Massive scale, ML focus, creator-oriented",
                "tips": "Know video processing. Discuss recommendations. Global scale. ML systems. Creator experience."
            },
            "Behavioral": {
                "focus": "Creator focus, innovation, global impact",
                "common_questions": ["How would you improve YouTube?", "Tell me about video systems", "Describe recommendations", "How do you help creators?"],
                "style": "Creator-focused, innovation-driven"
            },
            "System Design": {
                "focus": "Video platform, recommendations, global scale",
                "common_topics": ["Design video platform", "Design recommendation system", "Design global CDN"],
                "style": "Focus on scale and creator experience"
            }
        },
        "red_flags": ["Weak ML knowledge", "Ignoring scale", "Not creator-focused"],
        "average_process_duration": "6-10 weeks",
        "interview_count": "6-8 rounds"
    },
    
    "Snap (Snapchat)": {
        "name": "Snap (Snapchat)",
        "industry": "Social Media/AR",
        "size": "Medium (5000-10000)",
        "interview_style": "ar-and-mobile-first",
        "difficulty_level": "Very High",
        "cultural_values": ["Innovation", "Speed", "Quality", "Kindness", "Creativity"],
        "interview_rounds": {
            "Technical": {
                "focus": "AR, mobile-first, real-time, computer vision, ML",
                "common_topics": ["AR", "Computer vision", "Mobile apps", "Real-time systems", "ML"],
                "style": "AR focus, mobile-first, innovation-driven",
                "tips": "Know AR and computer vision. Discuss mobile optimization. Real-time systems. Innovation."
            },
            "Behavioral": {
                "focus": "Innovation, speed, creativity",
                "common_questions": ["How would you improve Snapchat?", "Tell me about AR projects", "Describe mobile optimization", "How do you innovate?"],
                "style": "Innovation-focused, creative, fast-paced"
            },
            "System Design": {
                "focus": "AR, mobile, real-time, computer vision",
                "common_topics": ["Design AR system", "Design mobile app", "Design real-time messaging"],
                "style": "Focus on AR and mobile innovation"
            }
        },
        "red_flags": ["Weak AR knowledge", "Not mobile-first", "Slow execution"],
        "average_process_duration": "6-8 weeks",
        "interview_count": "5-7 rounds"
    },
    
    "Pinterest": {
        "name": "Pinterest",
        "industry": "Social Media/Visual Discovery",
        "size": "Medium (3000-5000)",
        "interview_style": "visual-discovery-focused",
        "difficulty_level": "High",
        "cultural_values": ["Pinner first", "Innovation", "Inclusion", "Collaboration", "Excellence"],
        "interview_rounds": {
            "Technical": {
                "focus": "Visual search, recommendations, computer vision, ML, mobile",
                "common_topics": ["Computer vision", "Visual search", "Recommendation systems", "ML", "Mobile"],
                "style": "Visual discovery focus, ML-driven",
                "tips": "Know computer vision. Discuss visual search. Recommendation systems. ML."
            },
            "Behavioral": {
                "focus": "Pinner focus, innovation, inclusion",
                "common_questions": ["How would you improve Pinterest?", "Tell me about visual search", "Describe recommendations", "How do you innovate?"],
                "style": "Pinner-focused, inclusive, innovation-driven"
            },
            "System Design": {
                "focus": "Visual search, recommendations, computer vision",
                "common_topics": ["Design visual search", "Design recommendation system", "Design image processing"],
                "style": "Focus on visual discovery and ML"
            }
        },
        "red_flags": ["Weak CV knowledge", "Not pinner-focused", "Ignoring ML"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "5-6 rounds"
    },
    
    "Reddit": {
        "name": "Reddit",
        "industry": "Social Media/Community",
        "size": "Medium (2000-3000)",
        "interview_style": "community-focused",
        "difficulty_level": "High",
        "cultural_values": ["Community first", "Authenticity", "Innovation", "Transparency", "Inclusion"],
        "interview_rounds": {
            "Technical": {
                "focus": "Community platform, moderation, recommendations, mobile",
                "common_topics": ["Community systems", "Content moderation", "Recommendation systems", "Mobile apps", "Scale"],
                "style": "Community focus, authenticity-driven",
                "tips": "Know community dynamics. Discuss moderation. Recommendations. Authenticity."
            },
            "Behavioral": {
                "focus": "Community focus, authenticity, transparency",
                "common_questions": ["How would you improve Reddit?", "Tell me about community moderation", "Describe authenticity", "How do you innovate?"],
                "style": "Community-focused, authentic, transparent"
            },
            "System Design": {
                "focus": "Community platform, moderation, recommendations",
                "common_topics": ["Design community platform", "Design moderation system", "Design recommendation engine"],
                "style": "Focus on community and authenticity"
            }
        },
        "red_flags": ["Not community-focused", "Ignoring authenticity", "Weak moderation knowledge"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "4-5 rounds"
    },
    
    # ========== MORE FOOD DELIVERY (Target: 10+) ==========
    "Deliveroo": {
        "name": "Deliveroo",
        "industry": "Food Delivery/Logistics",
        "size": "Medium (3000-5000)",
        "interview_style": "logistics-and-marketplace",
        "difficulty_level": "High",
        "cultural_values": ["Customer obsession", "Innovation", "Ownership", "Excellence", "Collaboration"],
        "interview_rounds": {
            "Technical": {
                "focus": "Food delivery, logistics, routing, marketplace, mobile",
                "common_topics": ["Routing algorithms", "Marketplace", "Real-time matching", "Mobile apps", "Logistics"],
                "style": "Logistics focus, marketplace-oriented",
                "tips": "Know logistics and routing. Discuss marketplace dynamics. Real-time systems. Mobile."
            },
            "Behavioral": {
                "focus": "Customer obsession, ownership, innovation",
                "common_questions": ["How would you improve delivery times?", "Tell me about logistics optimization", "Describe marketplace", "How do you own projects?"],
                "style": "Customer-focused, ownership-driven"
            },
            "System Design": {
                "focus": "Food delivery, routing, marketplace",
                "common_topics": ["Design delivery system", "Design routing", "Design marketplace"],
                "style": "Focus on logistics and customer experience"
            }
        },
        "red_flags": ["Weak logistics knowledge", "Not customer-focused", "Slow execution"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Grubhub": {
        "name": "Grubhub",
        "industry": "Food Delivery/Marketplace",
        "size": "Medium (2000-3000)",
        "interview_style": "marketplace-focused",
        "difficulty_level": "Medium-High",
        "cultural_values": ["Customer focus", "Innovation", "Collaboration", "Excellence", "Integrity"],
        "interview_rounds": {
            "Technical": {
                "focus": "Food delivery, marketplace, mobile, logistics",
                "common_topics": ["Marketplace", "Mobile apps", "Logistics", "Search", "Recommendations"],
                "style": "Marketplace focus, mobile-first",
                "tips": "Know marketplace dynamics. Discuss mobile experience. Logistics. Search and recommendations."
            },
            "Behavioral": {
                "focus": "Customer focus, innovation, collaboration",
                "common_questions": ["How would you improve Grubhub?", "Tell me about marketplace", "Describe logistics", "How do you innovate?"],
                "style": "Customer-focused, collaborative"
            },
            "System Design": {
                "focus": "Marketplace, mobile, logistics",
                "common_topics": ["Design marketplace", "Design mobile app", "Design logistics"],
                "style": "Focus on marketplace and customer experience"
            }
        },
        "red_flags": ["Weak marketplace knowledge", "Not customer-focused", "Ignoring mobile"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "4 rounds"
    }
}

# ============================================
# BATCH ADD FUNCTION
# ============================================

def batch_add_companies():
    """Add all perfect-balance companies to the database"""
    
    # Load existing data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'data', 'company_profiles.json')
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("="*60)
    print("BATCH ADDING COMPANIES - ROUND 6 (PERFECT BALANCE)")
    print("="*60)
    print(f"\nCompanies to add: {len(COMPANIES_TO_ADD)}")
    print("\nAchieving 10+ companies per domain:")
    print("  - Gaming: +6 (Activision, Valve, EA, Ubisoft, Supercell, Krafton)")
    print("  - Cybersecurity: +6 (Fortinet, Check Point, Splunk, Rapid7, Darktrace, Tanium)")
    print("  - Healthcare: +7 (Philips, Medtronic, GE, Siemens, Athenahealth, Zocdoc, 1mg)")
    print("  - Travel: +6 (Tripadvisor, Kayak, MakeMyTrip, Hopper, Skyscanner, Ctrip)")
    print("  - Media: +4 (YouTube, Snap, Pinterest, Reddit)")
    print("  - Food Delivery: +2 (Deliveroo, Grubhub)")
    
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
    data['meta']['version'] = "6.0.0"
    
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
