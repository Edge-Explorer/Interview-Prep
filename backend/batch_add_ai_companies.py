"""
Batch script to add AI/ML companies - Round 3
Focus: OpenAI, Anthropic, DeepMind, Hugging Face, etc.
"""

import json
import os

# ============================================
# AI COMPANIES TO ADD
# ============================================

COMPANIES_TO_ADD = {
    "OpenAI": {
        "name": "OpenAI",
        "industry": "Artificial Intelligence/Research",
        "size": "Medium (500-1000)",
        "interview_style": "research-and-engineering-excellence",
        "difficulty_level": "Very High",
        "cultural_values": [
            "AGI safety",
            "Broad benefit",
            "Long-term thinking",
            "Collaboration",
            "Technical excellence"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "ML/AI, research, systems engineering, Python/C++",
                "common_topics": ["Deep learning", "Transformers", "Reinforcement learning", "Distributed systems", "GPU optimization"],
                "style": "Extremely rigorous, research-level depth required",
                "tips": "Know latest AI research. Discuss safety and alignment. Strong ML fundamentals. Read their papers."
            },
            "Behavioral": {
                "focus": "Mission alignment, collaboration, safety-consciousness",
                "common_questions": [
                    "Why OpenAI? Why AGI safety matters to you?",
                    "Tell me about your most impactful ML project",
                    "How do you think about AI alignment?",
                    "Describe a time you collaborated on research"
                ],
                "style": "Mission-driven, focus on safety and long-term thinking"
            },
            "System Design": {
                "focus": "ML infrastructure, training at scale, inference optimization",
                "common_topics": ["Design LLM training pipeline", "Design inference system", "Design RLHF system"],
                "style": "Focus on scale, efficiency, and safety"
            }
        },
        "red_flags": ["Not understanding AI safety", "Weak ML fundamentals", "Not mission-aligned", "Ignoring ethical implications"],
        "average_process_duration": "6-10 weeks",
        "interview_count": "6-8 rounds"
    },
    
    "Anthropic": {
        "name": "Anthropic",
        "industry": "Artificial Intelligence/AI Safety",
        "size": "Medium (100-500)",
        "interview_style": "safety-first-research",
        "difficulty_level": "Very High",
        "cultural_values": [
            "AI safety",
            "Responsible scaling",
            "Research excellence",
            "Transparency",
            "Long-term thinking"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "AI safety, interpretability, alignment, ML research",
                "common_topics": ["Constitutional AI", "RLHF", "Interpretability", "Alignment research", "Transformer architectures"],
                "style": "Research-heavy, safety-focused, extremely rigorous",
                "tips": "Read Anthropic's research papers. Discuss AI safety deeply. Know interpretability methods. Strong research background."
            },
            "Behavioral": {
                "focus": "Safety mindset, research collaboration, mission alignment",
                "common_questions": [
                    "Why AI safety? Why Anthropic?",
                    "Tell me about your research on AI alignment",
                    "How do you approach responsible AI development?",
                    "Describe your thoughts on Constitutional AI"
                ],
                "style": "Deeply mission-driven, focus on safety and responsibility"
            },
            "System Design": {
                "focus": "Safe AI systems, interpretability tools, alignment",
                "common_topics": ["Design safe LLM system", "Design interpretability framework", "Design RLHF pipeline"],
                "style": "Safety-first approach to all design decisions"
            }
        },
        "red_flags": ["Not safety-conscious", "Weak alignment understanding", "Not research-oriented", "Moving fast without thinking"],
        "average_process_duration": "6-10 weeks",
        "interview_count": "6-8 rounds"
    },
    
    "Google DeepMind": {
        "name": "Google DeepMind",
        "industry": "Artificial Intelligence/Research",
        "size": "Large (1000-5000)",
        "interview_style": "research-excellence",
        "difficulty_level": "Very High",
        "cultural_values": [
            "Solve intelligence",
            "Use it to make the world a better place",
            "Scientific rigor",
            "Collaboration",
            "Bold ambition"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "AI research, deep learning, reinforcement learning, neuroscience",
                "common_topics": ["Deep RL", "AlphaGo/AlphaFold", "Transformers", "Multi-agent systems", "Neuroscience-inspired AI"],
                "style": "World-class research level, PhD-level depth",
                "tips": "Know their landmark papers (AlphaGo, AlphaFold, Gemini). Strong research background. Discuss AGI path."
            },
            "Behavioral": {
                "focus": "Research impact, collaboration, scientific thinking",
                "common_questions": [
                    "Why DeepMind? What excites you about AGI?",
                    "Tell me about your most impactful research",
                    "How do you approach unsolved problems?",
                    "Describe a collaborative research project"
                ],
                "style": "Research-focused, emphasis on scientific rigor and impact"
            },
            "System Design": {
                "focus": "AI research systems, large-scale training, novel architectures",
                "common_topics": ["Design RL training system", "Design multi-modal AI", "Design protein folding system"],
                "style": "Focus on novel research and scientific breakthroughs"
            }
        },
        "red_flags": ["Weak research background", "Not scientifically rigorous", "Lack of ambition", "Not collaborative"],
        "average_process_duration": "8-12 weeks",
        "interview_count": "6-8 rounds"
    },
    
    "Hugging Face": {
        "name": "Hugging Face",
        "industry": "AI/Machine Learning Platform",
        "size": "Medium (100-500)",
        "interview_style": "open-source-and-community",
        "difficulty_level": "High",
        "cultural_values": [
            "Open source",
            "Community first",
            "Democratize AI",
            "Transparency",
            "Collaboration"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "ML/NLP, transformers, open source, Python",
                "common_topics": ["Transformers", "NLP", "Model deployment", "Open source contributions", "Python/PyTorch"],
                "style": "Open source mindset, community-focused, practical ML",
                "tips": "Contribute to Hugging Face repos. Know transformers library deeply. Show open source passion. Community engagement."
            },
            "Behavioral": {
                "focus": "Open source values, community building, democratization",
                "common_questions": [
                    "Why open source? Why Hugging Face?",
                    "Tell me about your open source contributions",
                    "How would you help democratize AI?",
                    "Describe your community engagement"
                ],
                "style": "Community-driven, open source culture, inclusive"
            },
            "System Design": {
                "focus": "ML platform, model hub, inference optimization",
                "common_topics": ["Design model hub", "Design inference API", "Design training platform"],
                "style": "Focus on accessibility and community needs"
            }
        },
        "red_flags": ["Not open source minded", "Lack of community engagement", "Closed-source mentality", "Not collaborative"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Stability AI": {
        "name": "Stability AI",
        "industry": "AI/Generative AI",
        "size": "Medium (100-500)",
        "interview_style": "open-and-creative",
        "difficulty_level": "High",
        "cultural_values": [
            "Open AI",
            "Creativity",
            "Accessibility",
            "Innovation",
            "Community"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Generative AI, diffusion models, computer vision, open source",
                "common_topics": ["Stable Diffusion", "Diffusion models", "Image generation", "Model training", "Open source"],
                "style": "Creative + technical, open source mindset",
                "tips": "Know diffusion models. Discuss Stable Diffusion architecture. Show creative applications. Open source contributions."
            },
            "Behavioral": {
                "focus": "Creativity, open access, innovation",
                "common_questions": [
                    "Why generative AI? Why open models?",
                    "Tell me about a creative AI project",
                    "How do you think about AI accessibility?",
                    "Describe your vision for generative AI"
                ],
                "style": "Creative, open-minded, community-focused"
            },
            "System Design": {
                "focus": "Generative AI systems, image generation, model serving",
                "common_topics": ["Design image generation platform", "Design model training pipeline", "Design inference optimization"],
                "style": "Focus on creativity and accessibility"
            }
        },
        "red_flags": ["Not creative", "Closed-source mindset", "Weak generative AI knowledge", "Not community-focused"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Midjourney": {
        "name": "Midjourney",
        "industry": "AI/Generative Art",
        "size": "Small (<100)",
        "interview_style": "creative-and-technical",
        "difficulty_level": "Very High",
        "cultural_values": [
            "Creativity",
            "Quality",
            "Innovation",
            "Community",
            "Artistic vision"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Generative AI, diffusion models, aesthetics, community platforms",
                "common_topics": ["Image generation", "Diffusion models", "Aesthetic quality", "Discord bots", "Community tools"],
                "style": "Creative + technical excellence, high quality bar",
                "tips": "Show creative work. Discuss aesthetics and art. Know generative models. Community building experience."
            },
            "Behavioral": {
                "focus": "Creativity, quality obsession, community building",
                "common_questions": [
                    "Show me your creative AI projects",
                    "How do you think about aesthetic quality?",
                    "Tell me about community building",
                    "Describe your artistic vision for AI"
                ],
                "style": "Creative, quality-focused, community-oriented"
            },
            "System Design": {
                "focus": "Image generation, Discord integration, community platforms",
                "common_topics": ["Design image generation system", "Design Discord bot", "Design community platform"],
                "style": "Focus on quality, creativity, and community"
            }
        },
        "red_flags": ["Lack of creativity", "Poor aesthetic sense", "Not community-minded", "Low quality standards"],
        "average_process_duration": "5-7 weeks",
        "interview_count": "4-6 rounds"
    },
    
    "Cohere": {
        "name": "Cohere",
        "industry": "AI/Enterprise NLP",
        "size": "Medium (100-500)",
        "interview_style": "enterprise-ai-focused",
        "difficulty_level": "High",
        "cultural_values": [
            "Customer success",
            "Innovation",
            "Responsibility",
            "Collaboration",
            "Excellence"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "NLP, LLMs, enterprise AI, API design",
                "common_topics": ["Language models", "NLP", "Enterprise AI", "API design", "Model deployment"],
                "style": "Enterprise-focused, practical AI applications",
                "tips": "Know enterprise AI needs. Discuss LLMs and NLP. Show customer focus. API design skills."
            },
            "Behavioral": {
                "focus": "Customer success, responsibility, collaboration",
                "common_questions": [
                    "How do you approach enterprise AI?",
                    "Tell me about deploying AI for customers",
                    "Describe your approach to responsible AI",
                    "How do you handle customer requirements?"
                ],
                "style": "Customer-focused, responsible AI mindset"
            },
            "System Design": {
                "focus": "Enterprise NLP platform, API design, scalability",
                "common_topics": ["Design NLP API", "Design enterprise AI platform", "Design model serving"],
                "style": "Focus on enterprise needs and reliability"
            }
        },
        "red_flags": ["Not customer-focused", "Weak NLP knowledge", "Ignoring enterprise needs", "Not responsible"],
        "average_process_duration": "5-6 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Scale AI": {
        "name": "Scale AI",
        "industry": "AI/Data Infrastructure",
        "size": "Medium (500-1000)",
        "interview_style": "data-and-ml-ops",
        "difficulty_level": "High",
        "cultural_values": [
            "Customer obsession",
            "Bias for action",
            "Ownership",
            "Excellence",
            "Innovation"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "ML ops, data pipelines, labeling, infrastructure",
                "common_topics": ["Data labeling", "ML pipelines", "Quality control", "Infrastructure", "Computer vision/NLP"],
                "style": "Practical ML ops, focus on data quality and scale",
                "tips": "Understand data labeling challenges. Discuss ML ops. Show infrastructure skills. Quality obsession."
            },
            "Behavioral": {
                "focus": "Customer obsession, ownership, bias for action",
                "common_questions": [
                    "How do you ensure data quality?",
                    "Tell me about scaling ML infrastructure",
                    "Describe a time you owned a complex project",
                    "How do you handle customer needs?"
                ],
                "style": "Fast-paced, customer-focused, ownership culture"
            },
            "System Design": {
                "focus": "Data labeling platform, ML ops, quality control",
                "common_topics": ["Design labeling platform", "Design ML pipeline", "Design quality control system"],
                "style": "Focus on scale, quality, and customer needs"
            }
        },
        "red_flags": ["Poor data quality awareness", "Lack of ownership", "Not customer-focused", "Slow execution"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "4-5 rounds"
    },
    
    "Perplexity AI": {
        "name": "Perplexity AI",
        "industry": "AI/Search",
        "size": "Small (50-100)",
        "interview_style": "product-and-ai-focused",
        "difficulty_level": "High",
        "cultural_values": [
            "Truth-seeking",
            "Speed",
            "Quality",
            "Innovation",
            "User focus"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "LLMs, search, retrieval, product engineering",
                "common_topics": ["RAG (Retrieval-Augmented Generation)", "Search algorithms", "LLMs", "Real-time systems"],
                "style": "Product-focused AI engineering, speed and quality",
                "tips": "Know RAG deeply. Discuss search and retrieval. Show product sense. Speed of execution."
            },
            "Behavioral": {
                "focus": "Truth-seeking, speed, user focus",
                "common_questions": [
                    "How would you improve Perplexity?",
                    "Tell me about building AI products",
                    "Describe your approach to search and retrieval",
                    "How do you ensure answer quality?"
                ],
                "style": "Product-focused, fast-paced, quality-obsessed"
            },
            "System Design": {
                "focus": "AI search, RAG systems, real-time retrieval",
                "common_topics": ["Design AI search engine", "Design RAG system", "Design citation system"],
                "style": "Focus on speed, accuracy, and user experience"
            }
        },
        "red_flags": ["Weak RAG knowledge", "Slow execution", "Not product-focused", "Poor quality standards"],
        "average_process_duration": "3-5 weeks",
        "interview_count": "4 rounds"
    },
    
    "Character.AI": {
        "name": "Character.AI",
        "industry": "AI/Conversational AI",
        "size": "Small (50-100)",
        "interview_style": "conversational-ai-focused",
        "difficulty_level": "High",
        "cultural_values": [
            "User delight",
            "Innovation",
            "Creativity",
            "Quality",
            "Community"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "LLMs, conversational AI, personalization, scale",
                "common_topics": ["Dialogue systems", "LLM fine-tuning", "Personalization", "Real-time inference"],
                "style": "Focus on conversational AI and user experience",
                "tips": "Know dialogue systems. Discuss personalization. Show creativity. User experience focus."
            },
            "Behavioral": {
                "focus": "User delight, creativity, innovation",
                "common_questions": [
                    "How would you improve character conversations?",
                    "Tell me about building conversational AI",
                    "Describe your approach to personalization",
                    "How do you create delightful experiences?"
                ],
                "style": "Creative, user-focused, innovation-driven"
            },
            "System Design": {
                "focus": "Conversational AI platform, personalization, scale",
                "common_topics": ["Design chat system", "Design character memory", "Design personalization engine"],
                "style": "Focus on user experience and conversational quality"
            }
        },
        "red_flags": ["Weak conversational AI knowledge", "Not user-focused", "Lack of creativity", "Poor UX sense"],
        "average_process_duration": "4-5 weeks",
        "interview_count": "4 rounds"
    },
    
    "Runway": {
        "name": "Runway",
        "industry": "AI/Creative Tools",
        "size": "Small (50-100)",
        "interview_style": "creative-ai-focused",
        "difficulty_level": "High",
        "cultural_values": [
            "Creativity",
            "Innovation",
            "Quality",
            "Accessibility",
            "Artistic vision"
        ],
        "interview_rounds": {
            "Technical": {
                "focus": "Generative AI, video generation, creative tools, real-time",
                "common_topics": ["Video generation", "Diffusion models", "Real-time AI", "Creative tools", "Computer vision"],
                "style": "Creative + technical, focus on artistic applications",
                "tips": "Show creative AI projects. Know video generation. Discuss real-time systems. Artistic sensibility."
            },
            "Behavioral": {
                "focus": "Creativity, innovation, artistic vision",
                "common_questions": [
                    "Show me your creative AI work",
                    "How do you think about AI for creators?",
                    "Tell me about building creative tools",
                    "Describe your artistic vision"
                ],
                "style": "Creative, artistic, innovation-focused"
            },
            "System Design": {
                "focus": "Creative AI tools, video generation, real-time processing",
                "common_topics": ["Design video generation system", "Design creative editing tool", "Design real-time AI"],
                "style": "Focus on creativity and user experience"
            }
        },
        "red_flags": ["Lack of creativity", "Poor artistic sense", "Not user-focused", "Weak generative AI knowledge"],
        "average_process_duration": "4-6 weeks",
        "interview_count": "4-5 rounds"
    }
}

# ============================================
# BATCH ADD FUNCTION
# ============================================

def batch_add_companies():
    """Add all AI companies to the database"""
    
    # Load existing data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'data', 'company_profiles.json')
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("="*60)
    print("BATCH ADDING AI COMPANIES - ROUND 3")
    print("="*60)
    print(f"\nAI Companies to add: {len(COMPANIES_TO_ADD)}")
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
    data['meta']['version'] = "3.1.0"
    
    # Save updated data
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"✅ Successfully added {added_count} AI companies!")
    print(f"📊 Total companies now: {data['meta']['total_companies']}")
    print(f"{'='*60}")
    print(f"\n💡 Test it by running: python test_company_intel.py")

if __name__ == "__main__":
    batch_add_companies()
