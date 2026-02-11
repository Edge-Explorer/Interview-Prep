"""
Batch script to add multiple companies at once
Run: python batch_add_companies.py
"""

import json
import os

# ============================================
# COMPANIES TO ADD
# ============================================

COMPANIES_TO_ADD = {
    # ========== FAANG-TIER ==========
    "Nvidia": {
        "name": "Nvidia",
        "industry": "Technology/Hardware/AI",
        "size": "Large (>10000)",
        "interview_style": "technical-depth-heavy",
        "difficulty_level": "Very High",
        "cultural_values": [
            "Innovation",
            "Excellence",
            "Speed",
            "Teamwork",
            "Intellectual honesty"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "GPU programming, parallel computing, deep learning, C++/CUDA",
                "common_topics": ["CUDA programming", "Parallel algorithms", "Computer architecture", "Deep learning optimization"],
                "style": "Deep technical dive, focus on low-level optimization",
                "tips": "Know GPU architecture. Discuss parallelization and optimization."
            },
            "Behavioral": {
                "focus": "Innovation, teamwork, technical excellence",
                "common_questions": [
                    "Tell me about a time you optimized performance",
                    "How do you stay updated with AI/GPU technology?",
                    "Describe a challenging technical problem you solved"
                ],
                "style": "Technical depth + cultural fit"
            },
            "System Design": {
                "focus": "High-performance computing, AI infrastructure, GPU optimization",
                "common_topics": ["Design ML training pipeline", "Design GPU cluster", "Design inference system"],
                "style": "Focus on performance and parallelization"
            }
        },
        "red_flags": ["Weak C++ skills", "Not understanding parallelization", "Lack of hardware knowledge"],
        "average_process_duration": "6-8 weeks",
        "interview_count": "5-6 rounds"
    },
    
    "Oracle": {
        "name": "Oracle",
        "industry": "Technology/Enterprise Software",
        "size": "Large (>100000)",
        "interview_style": "database-and-enterprise-focused",
        "difficulty_level": "High",
        "cultural_values": [
            "Customer success",
            "Innovation",
            "Integrity",
            "Teamwork",
            "Excellence"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Databases, SQL, enterprise systems, Java",
                "common_topics": ["SQL optimization", "Database design", "Java/OOP", "Enterprise architecture"],
                "style": "Strong focus on databases and enterprise solutions",
                "tips": "Master SQL. Know database internals. Discuss enterprise scale."
            },
            "Behavioral": {
                "focus": "Customer focus, teamwork, enterprise mindset",
                "common_questions": [
                    "How do you handle enterprise customer requirements?",
                    "Tell me about a time you worked on a large-scale system",
                    "Describe your approach to database optimization"
                ],
                "style": "Professional, focus on enterprise experience"
            },
            "System Design": {
                "focus": "Enterprise systems, databases, high availability",
                "common_topics": ["Design enterprise database", "Design backup system", "Design multi-tenant architecture"],
                "style": "Focus on reliability and enterprise requirements"
            }
        },
        "red_flags": ["Weak SQL skills", "Not understanding enterprise needs", "Lack of database knowledge"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "IBM": {
        "name": "IBM",
        "industry": "Technology/Enterprise Services",
        "size": "Large (>100000)",
        "interview_style": "enterprise-and-consulting",
        "difficulty_level": "Medium-High",
        "cultural_values": [
            "Innovation",
            "Trust and responsibility",
            "Client success",
            "Restless reinvention",
            "Inclusion"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Enterprise systems, cloud, AI, consulting",
                "common_topics": ["Cloud architecture", "AI/ML", "Enterprise integration", "Legacy systems"],
                "style": "Balanced technical + business understanding",
                "tips": "Show enterprise experience. Discuss client needs."
            },
            "Behavioral": {
                "focus": "Client focus, adaptability, innovation",
                "common_questions": [
                    "How do you handle client requirements?",
                    "Tell me about a time you modernized a legacy system",
                    "Describe your approach to innovation"
                ],
                "style": "Professional, focus on client impact"
            },
            "System Design": {
                "focus": "Enterprise architecture, cloud, hybrid systems",
                "common_topics": ["Design hybrid cloud", "Design enterprise migration", "Design AI platform"],
                "style": "Focus on enterprise and legacy integration"
            }
        },
        "red_flags": ["Not understanding enterprise", "Lack of client focus", "Resistance to change"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "3-4 rounds"
    },
    
    # ========== INDIAN TECH ==========
    "Ola": {
        "name": "Ola",
        "industry": "Technology/Transportation",
        "size": "Large (5000-10000)",
        "interview_style": "scale-and-execution",
        "difficulty_level": "High",
        "cultural_values": [
            "Customer first",
            "Ownership",
            "Innovation",
            "Integrity",
            "Speed"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Real-time systems, maps, routing, mobile-first",
                "common_topics": ["Routing algorithms", "Real-time tracking", "Maps integration", "Mobile optimization"],
                "style": "Practical problem-solving, India-scale focus",
                "tips": "Think about India-specific challenges. Discuss scale and mobile-first."
            },
            "Behavioral": {
                "focus": "Ownership, speed, customer obsession",
                "common_questions": [
                    "How would you improve Ola's ETA accuracy?",
                    "Tell me about a time you moved fast",
                    "Describe a customer problem you solved"
                ],
                "style": "Fast-paced, focus on execution"
            },
            "System Design": {
                "focus": "Ride-hailing, real-time matching, logistics",
                "common_topics": ["Design ride matching", "Design surge pricing", "Design driver allocation"],
                "style": "Focus on real-time and India-scale"
            }
        },
        "red_flags": ["Slow execution", "Not understanding Indian market", "Lack of ownership"],
        "average_process_duration": "3-4 weeks",
        "interview_count": "3-4 rounds"
    },
    
    "PhonePe": {
        "name": "PhonePe",
        "industry": "Fintech/Payments",
        "size": "Medium (5000-10000)",
        "interview_style": "scale-and-reliability",
        "difficulty_level": "High",
        "cultural_values": [
            "Customer obsession",
            "Ownership",
            "Speed",
            "Innovation",
            "Integrity"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Payment systems, UPI, scale, reliability",
                "common_topics": ["UPI integration", "Payment processing", "High availability", "Mobile-first"],
                "style": "Focus on reliability and India-scale",
                "tips": "Know UPI. Discuss handling millions of transactions. Zero downtime."
            },
            "Behavioral": {
                "focus": "Ownership, customer focus, speed",
                "common_questions": [
                    "How do you ensure payment reliability?",
                    "Tell me about a time you handled a production incident",
                    "Describe your approach to scaling"
                ],
                "style": "Action-oriented, focus on reliability"
            },
            "System Design": {
                "focus": "Payment systems, UPI, high availability",
                "common_topics": ["Design UPI payment", "Design wallet system", "Design transaction reconciliation"],
                "style": "Zero tolerance for errors, focus on reliability"
            }
        },
        "red_flags": ["Not understanding payments", "Ignoring reliability", "Lack of India-market knowledge"],
        "average_process_duration": "3-4 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Meesho": {
        "name": "Meesho",
        "industry": "E-commerce/Social Commerce",
        "size": "Medium (1000-5000)",
        "interview_style": "product-and-scale",
        "difficulty_level": "Medium-High",
        "cultural_values": [
            "Customer obsession",
            "Ownership",
            "Frugality",
            "Innovation",
            "Inclusion"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Social commerce, mobile-first, tier-2/3 cities",
                "common_topics": ["Mobile optimization", "Low-bandwidth solutions", "Social features", "E-commerce systems"],
                "style": "Focus on Bharat (tier-2/3 cities) and mobile-first",
                "tips": "Think about low-end devices. Discuss vernacular support."
            },
            "Behavioral": {
                "focus": "Customer empathy, frugality, innovation",
                "common_questions": [
                    "How would you design for tier-3 city users?",
                    "Tell me about a time you built with constraints",
                    "Describe your approach to mobile-first design"
                ],
                "style": "Product-focused, empathy for Bharat users"
            },
            "System Design": {
                "focus": "Social commerce, mobile-first, low-bandwidth",
                "common_topics": ["Design social commerce platform", "Design reseller network", "Design low-bandwidth app"],
                "style": "Focus on Bharat market and constraints"
            }
        },
        "red_flags": ["Not understanding Bharat market", "Overengineering", "Lack of empathy"],
        "average_process_duration": "2-3 weeks",
        "interview_count": "3-4 rounds"
    },
    
    # ========== FINTECH ==========
    "Robinhood": {
        "name": "Robinhood",
        "industry": "Fintech/Trading",
        "size": "Medium (1000-5000)",
        "interview_style": "technical-rigor-and-reliability",
        "difficulty_level": "Very High",
        "cultural_values": [
            "Safety first",
            "Participation is power",
            "Radical customer focus",
            "First principles",
            "Continuous learning"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Trading systems, low-latency, financial accuracy",
                "common_topics": ["Real-time trading", "Order matching", "Market data", "Financial calculations"],
                "style": "Rigorous, zero tolerance for errors",
                "tips": "Know trading systems. Discuss latency and accuracy. Financial regulations."
            },
            "Behavioral": {
                "focus": "Customer focus, safety, first principles",
                "common_questions": [
                    "How do you ensure system reliability?",
                    "Tell me about a time you debugged a critical issue",
                    "Describe your approach to financial accuracy"
                ],
                "style": "Safety-first mindset, focus on customer impact"
            },
            "System Design": {
                "focus": "Trading platform, real-time data, reliability",
                "common_topics": ["Design trading platform", "Design order execution", "Design market data feed"],
                "style": "Focus on low-latency and zero errors"
            }
        },
        "red_flags": ["Not understanding trading", "Ignoring edge cases", "Lack of rigor"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "5-6 rounds"
    },
    
    "Coinbase": {
        "name": "Coinbase",
        "industry": "Fintech/Cryptocurrency",
        "size": "Medium (5000-10000)",
        "interview_style": "security-and-reliability-heavy",
        "difficulty_level": "Very High",
        "cultural_values": [
            "Clear communication",
            "Efficient execution",
            "Act with integrity",
            "Positive energy",
            "Continuous learning"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Blockchain, security, distributed systems, cryptography",
                "common_topics": ["Blockchain technology", "Cryptography", "Security", "Distributed systems"],
                "style": "Deep technical + security focus",
                "tips": "Know blockchain. Discuss security and cryptography. Zero tolerance for vulnerabilities."
            },
            "Behavioral": {
                "focus": "Integrity, execution, learning",
                "common_questions": [
                    "How do you ensure security in your code?",
                    "Tell me about a time you learned a new technology quickly",
                    "Describe your approach to crypto/blockchain"
                ],
                "style": "Focus on integrity and continuous learning"
            },
            "System Design": {
                "focus": "Cryptocurrency exchange, security, blockchain",
                "common_topics": ["Design crypto exchange", "Design wallet system", "Design trading engine"],
                "style": "Focus on security and distributed systems"
            }
        },
        "red_flags": ["Weak security knowledge", "Not understanding blockchain", "Lack of rigor"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "5-6 rounds"
    },
    
    # ========== CONSULTING ==========
    "Bain": {
        "name": "Bain & Company",
        "industry": "Management Consulting",
        "size": "Large (>10000)",
        "interview_style": "case-study-heavy",
        "difficulty_level": "Very High",
        "cultural_values": [
            "Results",
            "One team",
            "Client first",
            "Courage",
            "Respect"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Case interviews, business problem-solving, analytics",
                "common_topics": ["Market sizing", "Profitability", "Growth strategy", "Operations"],
                "style": "Interactive cases, structured problem-solving",
                "tips": "Practice case frameworks. Be structured. Show business acumen."
            },
            "Behavioral": {
                "focus": "Teamwork, results, client focus",
                "common_questions": [
                    "Tell me about a time you worked in a team",
                    "Describe your biggest achievement",
                    "How do you handle pressure?"
                ],
                "style": "Fit interview, focus on teamwork and results"
            }
        },
        "red_flags": ["Unstructured thinking", "Poor teamwork", "Lack of business sense"],
        "average_process_duration": "6-8 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Accenture": {
        "name": "Accenture",
        "industry": "Consulting/Technology Services",
        "size": "Large (>100000)",
        "interview_style": "competency-and-technical",
        "difficulty_level": "Medium",
        "cultural_values": [
            "Client value creation",
            "One global network",
            "Respect for the individual",
            "Best people",
            "Integrity",
            "Stewardship"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Technology consulting, domain knowledge, problem-solving",
                "common_topics": ["Cloud", "Digital transformation", "Coding basics", "Business analysis"],
                "style": "Competency-based, practical scenarios",
                "tips": "Show domain expertise. Discuss client impact. Know basics well."
            },
            "Behavioral": {
                "focus": "Client focus, teamwork, adaptability",
                "common_questions": [
                    "How do you handle client expectations?",
                    "Tell me about a time you adapted to change",
                    "Describe a team project"
                ],
                "style": "Competency-based, STAR method"
            }
        },
        "red_flags": ["Poor communication", "Lack of client focus", "Weak fundamentals"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "2-3 rounds"
    },
    
    # ========== STARTUPS ==========
    "Notion": {
        "name": "Notion",
        "industry": "Technology/Productivity Software",
        "size": "Small (500-1000)",
        "interview_style": "product-and-craft-focused",
        "difficulty_level": "High",
        "cultural_values": [
            "Craft",
            "User obsession",
            "Simplicity",
            "Thoughtfulness",
            "Ownership"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Product thinking, frontend/backend, craft",
                "common_topics": ["React", "Real-time collaboration", "Database design", "Product sense"],
                "style": "Craft-focused, emphasis on quality and user experience",
                "tips": "Show product sense. Discuss user experience. Attention to detail."
            },
            "Behavioral": {
                "focus": "Product thinking, craft, user obsession",
                "common_questions": [
                    "How would you improve Notion?",
                    "Tell me about a product you built with great attention to detail",
                    "Describe your approach to user experience"
                ],
                "style": "Product-focused, emphasis on craft and thoughtfulness"
            },
            "System Design": {
                "focus": "Real-time collaboration, document editing, sync",
                "common_topics": ["Design collaborative editor", "Design real-time sync", "Design offline-first app"],
                "style": "Focus on user experience and real-time systems"
            }
        },
        "red_flags": ["Lack of product sense", "Poor attention to detail", "Not user-focused"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Figma": {
        "name": "Figma",
        "industry": "Technology/Design Tools",
        "size": "Medium (1000-5000)",
        "interview_style": "design-and-technical-excellence",
        "difficulty_level": "Very High",
        "cultural_values": [
            "Make things better",
            "Move with urgency",
            "Communicate clearly",
            "Craft with pride",
            "Grow together"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Real-time collaboration, graphics, performance",
                "common_topics": ["WebGL", "Real-time sync", "CRDT", "Performance optimization"],
                "style": "Deep technical + design sensibility",
                "tips": "Know graphics and real-time systems. Discuss performance. Show design appreciation."
            },
            "Behavioral": {
                "focus": "Craft, urgency, collaboration",
                "common_questions": [
                    "How would you improve Figma?",
                    "Tell me about a time you optimized performance",
                    "Describe your approach to collaboration"
                ],
                "style": "Craft-focused, emphasis on quality and speed"
            },
            "System Design": {
                "focus": "Real-time collaboration, graphics rendering, design tools",
                "common_topics": ["Design collaborative canvas", "Design plugin system", "Design real-time sync"],
                "style": "Focus on performance and user experience"
            }
        },
        "red_flags": ["Weak performance optimization", "Lack of design sense", "Not collaborative"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "5-6 rounds"
    },
    
    "Vercel": {
        "name": "Vercel",
        "industry": "Technology/Developer Tools",
        "size": "Small (500-1000)",
        "interview_style": "developer-experience-focused",
        "difficulty_level": "High",
        "cultural_values": [
            "Developer first",
            "Move fast",
            "Quality",
            "Transparency",
            "Ownership"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Frontend, serverless, developer experience, performance",
                "common_topics": ["Next.js", "Serverless", "Edge computing", "Developer tools"],
                "style": "Developer-focused, emphasis on DX and performance",
                "tips": "Know Next.js and serverless. Discuss developer experience. Show performance focus."
            },
            "Behavioral": {
                "focus": "Developer empathy, speed, quality",
                "common_questions": [
                    "How would you improve Vercel's developer experience?",
                    "Tell me about a time you built developer tools",
                    "Describe your approach to performance"
                ],
                "style": "Developer-focused, emphasis on speed and quality"
            },
            "System Design": {
                "focus": "Serverless, edge computing, deployment platform",
                "common_topics": ["Design deployment platform", "Design edge network", "Design build system"],
                "style": "Focus on developer experience and performance"
            }
        },
        "red_flags": ["Not developer-focused", "Weak frontend skills", "Ignoring performance"],
        "average_process_duration": "4-5 weeks",
        "interview_count": "4 rounds"
    }
}

# ============================================
# BATCH ADD FUNCTION
# ============================================

def batch_add_companies():
    """Add all companies to the database"""
    
    # Load existing data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'data', 'company_profiles.json')
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("="*60)
    print("BATCH ADDING COMPANIES TO DATABASE")
    print("="*60)
    print(f"\nCompanies to add: {len(COMPANIES_TO_ADD)}")
    print("\nList:")
    for i, company in enumerate(COMPANIES_TO_ADD.keys(), 1):
        print(f"   {i}. {company}")
    
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
    data['meta']['version'] = "2.1.0"
    
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
