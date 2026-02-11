"""
Batch script to hit 10+ companies in every single domain
"""
import json
import os
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

COMPANIES_TO_ADD = {
    # ========== FOOD DELIVERY (Currently 6 -> Target 10+) ==========
    "Meituan": {
        "name": "Meituan",
        "industry": "Food Delivery/Super-app",
        "size": "Large (>100000)",
        "interview_style": "scale-unlimited",
        "difficulty_level": "Very High",
        "cultural_values": ["Customer centricity", "Integrity", "Excellence", "Win-win"],
        "interview_rounds": {
            "Technical": {
                "focus": "High-concurrency systems, massive logistics, algorithms",
                "common_topics": ["Distributed locking", "Logistics routing", "Dynamic pricing"]
            }
        },
        "red_flags": ["Not handling scale well", "Weak algorithm skills"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "4-5 rounds"
    },
    "Rappi": {
        "name": "Rappi",
        "industry": "Food Delivery/Logistics",
        "size": "Medium (5000-10000)",
        "interview_style": "hustle-and-growth",
        "difficulty_level": "High",
        "cultural_values": ["Drive", "Hustle", "Ownership", "Execution"],
        "interview_rounds": {
            "Technical": {
                "focus": "Real-time systems, mobile, logistics",
                "common_topics": ["Geofencing", "Live tracking", "Payment integration"]
            }
        },
        "red_flags": ["Slow execution mindset", "Lack of urgency"],
        "average_process_duration": "3-5 weeks",
        "interview_count": "4 rounds"
    },
    "Just Eat Takeaway": {
        "name": "Just Eat Takeaway",
        "industry": "Food Delivery",
        "size": "Large (15000-20000)",
        "interview_style": "global-consistency",
        "difficulty_level": "Medium-High",
        "cultural_values": ["Lead", "Care", "Deliver"],
        "interview_rounds": {
            "Technical": {
                "focus": "Microservices, scalability, global platform integration"
            }
        },
        "red_flags": ["Ignoring global scale", "Weak testing culture"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "4 rounds"
    },
    "Glovo": {
        "name": "Glovo",
        "industry": "Food Delivery/Anything",
        "size": "Medium (3000-5000)",
        "interview_style": "delivery-excellence",
        "difficulty_level": "High",
        "cultural_values": ["Care", "Glownership", "Gas", "Good vibes"],
        "interview_rounds": {
            "Technical": {
                "focus": "Multi-category delivery systems, routing optimization"
            }
        },
        "red_flags": ["Not thinking about the courier experience"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "4 rounds"
    },

    # ========== TRAVEL (Currently 9 -> Target 10+) ==========
    "Agoda": {
        "name": "Agoda",
        "industry": "Travel/OTA",
        "size": "Medium (5000-6000)",
        "interview_style": "data-obsessed",
        "difficulty_level": "High",
        "cultural_values": ["Be a scientist", "Be an owner", "Data-driven"],
        "interview_rounds": {
            "Technical": {
                "focus": "Performance, A/B testing, data engineering, backend scale",
                "common_topics": ["Latency optimization", "Experimentation frameworks"]
            }
        },
        "red_flags": ["Arguments without data", "Weak performance awareness"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "4-5 rounds"
    },

    # ========== MEDIA (Currently 9 -> Target 10+) ==========
    "Disney+ (Disney Streaming)": {
        "name": "Disney+ (Disney Streaming)",
        "industry": "Media/Streaming",
        "size": "Large (>5000)",
        "interview_style": "premium-streaming",
        "difficulty_level": "High",
        "cultural_values": ["Storytelling", "Quality", "Innovation", "Reliability"],
        "interview_rounds": {
            "Technical": {
                "focus": "Excellence in video delivery, global scale, reliability",
                "common_topics": ["DRM", "Video Player technology", "Cloud infrastructure"]
            }
        },
        "red_flags": ["Compromising quality", "Slow UI response"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "4-5 rounds"
    },
    "Hulu": {
        "name": "Hulu",
        "industry": "Media/Streaming",
        "size": "Medium (2000-3000)",
        "interview_style": "product-engineering",
        "difficulty_level": "High",
        "cultural_values": ["Hulugan spirit", "Collaboration", "Quality", "Customer obsession"],
        "interview_rounds": {
            "Technical": {
                "focus": "Backend services, low-latency APIs, content systems"
            }
        },
        "red_flags": ["Not collaborative", "Weak testing"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "4 rounds"
    }
}

def batch_add_companies():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'data', 'company_profiles.json')
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("="*60)
    print("BATCH ADDING COMPANIES - ROUND 8 (FINAL BALANCE)")
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
    data['meta']['version'] = "8.0.0"
    
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"\nSuccessfully added {added_count} companies!")
    print(f"Total companies now: {data['meta']['total_companies']}")

if __name__ == "__main__":
    batch_add_companies()
