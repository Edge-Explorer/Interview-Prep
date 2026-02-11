"""
Batch script to add MORE companies - Round 2
Adds 20 more companies to reach 65 total
"""

import json
import os

# ============================================
# COMPANIES TO ADD - ROUND 2
# ============================================

COMPANIES_TO_ADD = {
    # ========== MORE TECH GIANTS ==========
    "Intel": {
        "name": "Intel",
        "industry": "Technology/Semiconductors",
        "size": "Large (>100000)",
        "interview_style": "hardware-and-systems-focused",
        "difficulty_level": "High",
        "cultural_values": [
            "Customer first",
            "Fearless innovation",
            "Results driven",
            "One Intel",
            "Inclusion"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Computer architecture, hardware, low-level programming, C/C++",
                "common_topics": ["Computer architecture", "C/C++", "Embedded systems", "Hardware design"],
                "style": "Deep technical, focus on fundamentals and hardware",
                "tips": "Know computer architecture deeply. Strong C/C++ required. Discuss hardware-software interaction."
            },
            "Behavioral": {
                "focus": "Innovation, teamwork, customer focus",
                "common_questions": [
                    "Tell me about a time you innovated",
                    "How do you approach hardware-software co-design?",
                    "Describe a challenging technical problem"
                ],
                "style": "Professional, focus on technical depth"
            },
            "System Design": {
                "focus": "Hardware systems, chip design, performance",
                "common_topics": ["Design processor", "Design memory hierarchy", "Design embedded system"],
                "style": "Focus on hardware and low-level optimization"
            }
        },
        "red_flags": ["Weak C/C++", "Not understanding hardware", "Lack of fundamentals"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Cisco": {
        "name": "Cisco",
        "industry": "Technology/Networking",
        "size": "Large (>50000)",
        "interview_style": "networking-focused",
        "difficulty_level": "Medium-High",
        "cultural_values": [
            "Customer obsession",
            "Innovation",
            "Collaboration",
            "Integrity",
            "Inclusion"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Networking, protocols, distributed systems, C/Python",
                "common_topics": ["TCP/IP", "Routing protocols", "Network security", "SDN"],
                "style": "Strong networking fundamentals required",
                "tips": "Master networking protocols. Know OSI model. Discuss network design."
            },
            "Behavioral": {
                "focus": "Customer focus, collaboration, innovation",
                "common_questions": [
                    "How do you troubleshoot network issues?",
                    "Tell me about a time you worked with customers",
                    "Describe your approach to network design"
                ],
                "style": "Professional, focus on customer impact"
            },
            "System Design": {
                "focus": "Network architecture, routing, security",
                "common_topics": ["Design data center network", "Design VPN", "Design load balancer"],
                "style": "Focus on networking and scalability"
            }
        },
        "red_flags": ["Weak networking knowledge", "Not customer-focused", "Poor troubleshooting"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "3-4 rounds"
    },
    
    "SAP": {
        "name": "SAP",
        "industry": "Technology/Enterprise Software",
        "size": "Large (>100000)",
        "interview_style": "enterprise-and-business-focused",
        "difficulty_level": "Medium",
        "cultural_values": [
            "Customer focus",
            "Innovation",
            "Collaboration",
            "Integrity",
            "Diversity"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Enterprise systems, ERP, business processes, Java/ABAP",
                "common_topics": ["ERP systems", "Business processes", "Database", "Integration"],
                "style": "Business + technical understanding required",
                "tips": "Understand business processes. Know ERP concepts. Discuss enterprise scale."
            },
            "Behavioral": {
                "focus": "Customer focus, business acumen, teamwork",
                "common_questions": [
                    "How do you handle enterprise customer requirements?",
                    "Tell me about a complex business process you automated",
                    "Describe your approach to ERP implementation"
                ],
                "style": "Professional, focus on business value"
            },
            "System Design": {
                "focus": "Enterprise architecture, ERP, integration",
                "common_topics": ["Design ERP system", "Design integration platform", "Design business workflow"],
                "style": "Focus on business processes and enterprise scale"
            }
        },
        "red_flags": ["Lack of business understanding", "Not customer-focused", "Weak enterprise knowledge"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "3-4 rounds"
    },
    
    # ========== MORE INDIAN TECH ==========
    "Dream11": {
        "name": "Dream11",
        "industry": "Gaming/Fantasy Sports",
        "size": "Medium (1000-5000)",
        "interview_style": "scale-and-real-time",
        "difficulty_level": "High",
        "cultural_values": [
            "User first",
            "Ownership",
            "Innovation",
            "Integrity",
            "Speed"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Real-time systems, gaming, high concurrency, mobile-first",
                "common_topics": ["Real-time scoring", "High concurrency", "Mobile optimization", "Gaming algorithms"],
                "style": "Focus on scale and real-time performance",
                "tips": "Think about millions of concurrent users. Discuss real-time updates. Mobile-first."
            },
            "Behavioral": {
                "focus": "Ownership, speed, user focus",
                "common_questions": [
                    "How would you handle IPL match day traffic?",
                    "Tell me about a time you optimized for scale",
                    "Describe your approach to real-time systems"
                ],
                "style": "Fast-paced, focus on execution and scale"
            },
            "System Design": {
                "focus": "Fantasy sports, real-time scoring, high traffic",
                "common_topics": ["Design fantasy sports platform", "Design real-time leaderboard", "Design contest system"],
                "style": "Focus on real-time and India-scale traffic"
            }
        },
        "red_flags": ["Not understanding scale", "Slow execution", "Ignoring real-time constraints"],
        "average_process_duration": "3-4 weeks",
        "interview_count": "3-4 rounds"
    },
    
    "Byju's": {
        "name": "Byju's",
        "industry": "EdTech",
        "size": "Large (>10000)",
        "interview_style": "product-and-mobile-focused",
        "difficulty_level": "Medium-High",
        "cultural_values": [
            "Student first",
            "Innovation",
            "Ownership",
            "Excellence",
            "Impact"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Mobile apps, video streaming, personalization, analytics",
                "common_topics": ["Mobile development", "Video streaming", "Recommendation systems", "Analytics"],
                "style": "Product-focused, mobile-first",
                "tips": "Think about student experience. Discuss personalization. Mobile optimization."
            },
            "Behavioral": {
                "focus": "Student focus, innovation, impact",
                "common_questions": [
                    "How would you improve student engagement?",
                    "Tell me about a product you built for education",
                    "Describe your approach to personalization"
                ],
                "style": "Product-focused, emphasis on student impact"
            },
            "System Design": {
                "focus": "EdTech platform, video streaming, personalization",
                "common_topics": ["Design learning platform", "Design video delivery", "Design adaptive learning"],
                "style": "Focus on student experience and scale"
            }
        },
        "red_flags": ["Not student-focused", "Weak mobile skills", "Lack of product sense"],
        "average_process_duration": "3-4 weeks",
        "interview_count": "3-4 rounds"
    },
    
    "Udaan": {
        "name": "Udaan",
        "industry": "B2B E-commerce",
        "size": "Medium (1000-5000)",
        "interview_style": "scale-and-logistics",
        "difficulty_level": "Medium-High",
        "cultural_values": [
            "Customer obsession",
            "Ownership",
            "Frugality",
            "Innovation",
            "Execution"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "B2B commerce, logistics, supply chain, mobile-first",
                "common_topics": ["Inventory management", "Supply chain", "B2B workflows", "Mobile optimization"],
                "style": "Focus on B2B and tier-2/3 cities",
                "tips": "Understand B2B vs B2C. Discuss supply chain. Think tier-2/3 cities."
            },
            "Behavioral": {
                "focus": "Ownership, frugality, execution",
                "common_questions": [
                    "How would you solve for small retailers?",
                    "Tell me about a time you built with constraints",
                    "Describe your approach to B2B commerce"
                ],
                "style": "Practical, focus on execution and impact"
            },
            "System Design": {
                "focus": "B2B marketplace, inventory, logistics",
                "common_topics": ["Design B2B marketplace", "Design inventory system", "Design supply chain"],
                "style": "Focus on B2B workflows and scale"
            }
        },
        "red_flags": ["Not understanding B2B", "Overengineering", "Lack of frugality"],
        "average_process_duration": "2-3 weeks",
        "interview_count": "3-4 rounds"
    },
    
    # ========== MORE FINANCE ==========
    "Morgan Stanley": {
        "name": "Morgan Stanley",
        "industry": "Finance/Investment Banking",
        "size": "Large (>50000)",
        "interview_style": "technical-and-finance-heavy",
        "difficulty_level": "Very High",
        "cultural_values": [
            "Putting clients first",
            "Doing the right thing",
            "Leading with exceptional ideas",
            "Committing to diversity",
            "Giving back"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Algorithms, system design, financial systems, Java/C++",
                "common_topics": ["Low-latency systems", "Concurrency", "Financial modeling", "Trading systems"],
                "style": "Rigorous technical + finance knowledge",
                "tips": "Know finance basics. Discuss performance. Strong coding required."
            },
            "Behavioral": {
                "focus": "Client focus, integrity, leadership",
                "common_questions": [
                    "Why Morgan Stanley?",
                    "Tell me about a time you showed leadership",
                    "How do you handle market pressure?"
                ],
                "style": "Professional, focus on values and client impact"
            },
            "System Design": {
                "focus": "Trading systems, risk management, financial accuracy",
                "common_topics": ["Design trading platform", "Design risk system", "Design portfolio management"],
                "style": "Focus on accuracy, performance, compliance"
            }
        },
        "red_flags": ["Lack of finance knowledge", "Poor performance optimization", "Not detail-oriented"],
        "average_process_duration": "6-8 weeks",
        "interview_count": "5-6 rounds (including Superday)"
    },
    
    "Citadel": {
        "name": "Citadel",
        "industry": "Finance/Hedge Fund",
        "size": "Medium (5000-10000)",
        "interview_style": "extremely-technical",
        "difficulty_level": "Very High",
        "cultural_values": [
            "Excellence",
            "Collaboration",
            "Innovation",
            "Integrity",
            "Meritocracy"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Algorithms, math, low-latency, C++, quantitative skills",
                "common_topics": ["Advanced algorithms", "Probability", "C++", "Low-latency optimization"],
                "style": "Extremely rigorous, competitive programming level",
                "tips": "Practice competitive programming. Know C++ deeply. Strong math required."
            },
            "Behavioral": {
                "focus": "Excellence, collaboration, problem-solving",
                "common_questions": [
                    "Tell me about your most challenging technical problem",
                    "How do you optimize for performance?",
                    "Describe your approach to collaboration"
                ],
                "style": "Technical depth + cultural fit"
            },
            "System Design": {
                "focus": "Ultra-low-latency, trading systems, performance",
                "common_topics": ["Design HFT system", "Design order matching", "Design market data feed"],
                "style": "Focus on microsecond-level optimization"
            }
        },
        "red_flags": ["Weak algorithms", "Poor C++ skills", "Not performance-focused"],
        "average_process_duration": "6-10 weeks",
        "interview_count": "6-8 rounds"
    },
    
    # ========== MORE CONSULTING ==========
    "PwC": {
        "name": "PwC (PricewaterhouseCoopers)",
        "industry": "Consulting/Professional Services",
        "size": "Large (>100000)",
        "interview_style": "competency-based",
        "difficulty_level": "Medium",
        "cultural_values": [
            "Act with integrity",
            "Make a difference",
            "Care",
            "Work together",
            "Reimagine the possible"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Domain knowledge, problem-solving, business analysis",
                "common_topics": ["Business analysis", "Technology consulting", "Process improvement", "Data analytics"],
                "style": "Competency-based, practical scenarios",
                "tips": "Show domain expertise. Discuss client impact. Strong communication."
            },
            "Behavioral": {
                "focus": "Values, teamwork, client focus",
                "common_questions": [
                    "Tell me about a time you showed integrity",
                    "How do you handle difficult clients?",
                    "Describe a team project"
                ],
                "style": "STAR method, values-focused"
            }
        },
        "red_flags": ["Poor communication", "Lack of client focus", "Not values-aligned"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "2-3 rounds"
    },
    
    "KPMG": {
        "name": "KPMG",
        "industry": "Consulting/Professional Services",
        "size": "Large (>100000)",
        "interview_style": "competency-and-technical",
        "difficulty_level": "Medium",
        "cultural_values": [
            "Integrity",
            "Excellence",
            "Courage",
            "Together",
            "For Better"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Audit, consulting, technology, analytics",
                "common_topics": ["Financial analysis", "Technology consulting", "Data analytics", "Risk management"],
                "style": "Competency-based, focus on domain knowledge",
                "tips": "Know your domain well. Discuss client value. Strong analytical skills."
            },
            "Behavioral": {
                "focus": "Values, teamwork, excellence",
                "common_questions": [
                    "Tell me about a time you demonstrated excellence",
                    "How do you work in teams?",
                    "Describe a challenging client situation"
                ],
                "style": "STAR method, values-driven"
            }
        },
        "red_flags": ["Weak analytical skills", "Poor teamwork", "Lack of integrity"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "2-3 rounds"
    },
    
    # ========== MORE STARTUPS ==========
    "Linear": {
        "name": "Linear",
        "industry": "Technology/Project Management",
        "size": "Small (<100)",
        "interview_style": "craft-and-product-focused",
        "difficulty_level": "Very High",
        "cultural_values": [
            "Craft",
            "Speed",
            "Quality",
            "User focus",
            "Simplicity"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Frontend/backend, product thinking, performance, craft",
                "common_topics": ["React", "GraphQL", "Real-time systems", "Performance optimization"],
                "style": "Extremely high bar for craft and quality",
                "tips": "Show exceptional attention to detail. Discuss performance. Product sense required."
            },
            "Behavioral": {
                "focus": "Craft, product thinking, speed",
                "common_questions": [
                    "How would you improve Linear?",
                    "Tell me about a product you built with great craft",
                    "Describe your approach to performance"
                ],
                "style": "Product-focused, very high standards for quality"
            },
            "System Design": {
                "focus": "Project management tools, real-time, performance",
                "common_topics": ["Design issue tracker", "Design real-time collaboration", "Design keyboard shortcuts"],
                "style": "Focus on speed, craft, and user experience"
            }
        },
        "red_flags": ["Lack of craft", "Poor performance optimization", "Not product-focused"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "5-6 rounds"
    },
    
    "Supabase": {
        "name": "Supabase",
        "industry": "Technology/Backend-as-a-Service",
        "size": "Small (50-100)",
        "interview_style": "developer-experience-focused",
        "difficulty_level": "High",
        "cultural_values": [
            "Developer first",
            "Open source",
            "Quality",
            "Speed",
            "Transparency"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Databases, backend, developer tools, open source",
                "common_topics": ["PostgreSQL", "Backend systems", "Developer tools", "Open source"],
                "style": "Developer-focused, emphasis on DX and databases",
                "tips": "Know PostgreSQL deeply. Discuss developer experience. Open source contributions help."
            },
            "Behavioral": {
                "focus": "Developer empathy, open source, quality",
                "common_questions": [
                    "How would you improve Supabase's developer experience?",
                    "Tell me about your open source contributions",
                    "Describe your approach to database design"
                ],
                "style": "Developer-focused, open source mindset"
            },
            "System Design": {
                "focus": "Backend-as-a-service, databases, developer tools",
                "common_topics": ["Design BaaS platform", "Design database service", "Design auth system"],
                "style": "Focus on developer experience and databases"
            }
        },
        "red_flags": ["Weak database knowledge", "Not developer-focused", "Closed-source mindset"],
        "average_process_duration": "4-5 weeks",
        "interview_count": "4 rounds"
    },
    
    "Clerk": {
        "name": "Clerk",
        "industry": "Technology/Authentication",
        "size": "Small (50-100)",
        "interview_style": "developer-experience-and-security",
        "difficulty_level": "High",
        "cultural_values": [
            "Developer first",
            "Security",
            "Quality",
            "Speed",
            "Simplicity"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Authentication, security, frontend/backend, developer tools",
                "common_topics": ["Auth systems", "Security", "React", "Developer experience"],
                "style": "Security + developer experience focus",
                "tips": "Know auth deeply. Discuss security best practices. Show DX focus."
            },
            "Behavioral": {
                "focus": "Developer empathy, security mindset, quality",
                "common_questions": [
                    "How would you improve Clerk's developer experience?",
                    "Tell me about a security issue you handled",
                    "Describe your approach to authentication"
                ],
                "style": "Developer-focused, security-conscious"
            },
            "System Design": {
                "focus": "Authentication systems, security, developer tools",
                "common_topics": ["Design auth system", "Design SSO", "Design user management"],
                "style": "Focus on security and developer experience"
            }
        },
        "red_flags": ["Weak security knowledge", "Not developer-focused", "Poor auth understanding"],
        "average_process_duration": "4-5 weeks",
        "interview_count": "4 rounds"
    },
    
    "Replicate": {
        "name": "Replicate",
        "industry": "Technology/AI Infrastructure",
        "size": "Small (<50)",
        "interview_style": "ml-and-infrastructure-focused",
        "difficulty_level": "Very High",
        "cultural_values": [
            "Developer first",
            "Quality",
            "Innovation",
            "Simplicity",
            "Open source"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "ML infrastructure, distributed systems, developer tools",
                "common_topics": ["ML deployment", "Containers", "Distributed systems", "Developer experience"],
                "style": "Deep technical + ML knowledge required",
                "tips": "Know ML deployment. Discuss infrastructure. Show DX focus."
            },
            "Behavioral": {
                "focus": "Developer empathy, innovation, quality",
                "common_questions": [
                    "How would you improve ML deployment?",
                    "Tell me about an ML infrastructure project",
                    "Describe your approach to developer tools"
                ],
                "style": "Technical depth + developer focus"
            },
            "System Design": {
                "focus": "ML infrastructure, model deployment, scalability",
                "common_topics": ["Design ML platform", "Design model serving", "Design GPU scheduling"],
                "style": "Focus on ML infrastructure and developer experience"
            }
        },
        "red_flags": ["Weak ML knowledge", "Not developer-focused", "Lack of infrastructure experience"],
        "average_process_duration": "5-6 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Postman": {
        "name": "Postman",
        "industry": "Technology/Developer Tools",
        "size": "Medium (500-1000)",
        "interview_style": "developer-experience-focused",
        "difficulty_level": "High",
        "cultural_values": [
            "API first",
            "Developer obsessed",
            "Quality",
            "Innovation",
            "Collaboration"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "APIs, developer tools, frontend/backend, testing",
                "common_topics": ["API design", "Testing", "Developer tools", "Collaboration features"],
                "style": "Developer-focused, emphasis on APIs and DX",
                "tips": "Master API design. Discuss developer workflows. Show product sense."
            },
            "Behavioral": {
                "focus": "Developer empathy, product thinking, collaboration",
                "common_questions": [
                    "How would you improve Postman?",
                    "Tell me about a developer tool you built",
                    "Describe your approach to API design"
                ],
                "style": "Developer-focused, product-oriented"
            },
            "System Design": {
                "focus": "API platform, collaboration, developer tools",
                "common_topics": ["Design API testing platform", "Design collaboration features", "Design API documentation"],
                "style": "Focus on developer experience and APIs"
            }
        },
        "red_flags": ["Weak API knowledge", "Not developer-focused", "Lack of product sense"],
        "average_process_duration": "4-5 weeks",
        "interview_count": "4 rounds"
    },
    
    "HashiCorp": {
        "name": "HashiCorp",
        "industry": "Technology/Infrastructure",
        "size": "Medium (1000-5000)",
        "interview_style": "infrastructure-and-oss-focused",
        "difficulty_level": "Very High",
        "cultural_values": [
            "Pragmatism",
            "Communication",
            "Kindness",
            "Integrity",
            "Craftsmanship"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Infrastructure, distributed systems, Go, open source",
                "common_topics": ["Terraform", "Kubernetes", "Distributed systems", "Infrastructure as Code"],
                "style": "Deep infrastructure knowledge, open source mindset",
                "tips": "Know infrastructure deeply. Go language preferred. Open source contributions help."
            },
            "Behavioral": {
                "focus": "Pragmatism, communication, craftsmanship",
                "common_questions": [
                    "Tell me about an infrastructure project you built",
                    "How do you approach distributed systems?",
                    "Describe your open source contributions"
                ],
                "style": "Technical depth + open source culture"
            },
            "System Design": {
                "focus": "Infrastructure tools, distributed systems, IaC",
                "common_topics": ["Design infrastructure platform", "Design service mesh", "Design secrets management"],
                "style": "Focus on infrastructure and distributed systems"
            }
        },
        "red_flags": ["Weak infrastructure knowledge", "Not open source minded", "Poor Go skills"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "5-6 rounds"
    },
    
    "Grafana Labs": {
        "name": "Grafana Labs",
        "industry": "Technology/Observability",
        "size": "Medium (500-1000)",
        "interview_style": "observability-and-oss-focused",
        "difficulty_level": "High",
        "cultural_values": [
            "Open source first",
            "Customer obsessed",
            "Quality",
            "Collaboration",
            "Remote-first"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Observability, monitoring, distributed systems, Go/TypeScript",
                "common_topics": ["Metrics", "Logging", "Tracing", "Time-series databases"],
                "style": "Deep observability knowledge, open source mindset",
                "tips": "Know observability deeply. Discuss monitoring at scale. Open source contributions help."
            },
            "Behavioral": {
                "focus": "Customer focus, open source, collaboration",
                "common_questions": [
                    "Tell me about an observability project",
                    "How do you approach monitoring at scale?",
                    "Describe your open source work"
                ],
                "style": "Technical + open source culture, remote-friendly"
            },
            "System Design": {
                "focus": "Observability platform, time-series, distributed systems",
                "common_topics": ["Design monitoring system", "Design metrics platform", "Design alerting"],
                "style": "Focus on observability and scale"
            }
        },
        "red_flags": ["Weak observability knowledge", "Not open source minded", "Poor distributed systems understanding"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "4-5 rounds"
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
    print("BATCH ADDING COMPANIES - ROUND 2")
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
    data['meta']['version'] = "3.0.0"
    
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
