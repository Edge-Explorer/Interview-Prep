# AUTHOR: Karan Shelar (GitHub: Edge-Explorer)
# PROJECT: InterviewAI - Advanced Intelligence System
# ROLE: Lead Architect & AI Engineer
import os
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional, Annotated
from typing_extensions import TypedDict

# LangChain / LangGraph imports
from langgraph.graph import StateGraph, END
from ddgs import DDGS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from rapidfuzz import process, fuzz

# Service imports
from .company_intelligence import get_company_intelligence
from .gemini_service import gemini_service

# TypedDict for the Agent State
class AgentState(TypedDict):
    company_name: str
    industry: Optional[str]
    job_description: Optional[str]
    research_data: Optional[str]
    is_synthetic: bool
    confidence_score: int
    generated_profile: Optional[Dict[str, Any]]
    is_valid: bool
    iterations: int
    sources: List[Dict[str, str]]
    search_query: Optional[str]
    audited_data: Optional[str]
    audit_log: List[str]
    error: Optional[str]

class IntelligenceService:
    def __init__(self):
        self.model = None
        # Lazy loading of local ML can be implemented here if HAS_LOCAL_ML is True

    async def router_node(self, state: AgentState):
        """
        Smart Router Agent Node:
        1. Analyzes company name ambiguity.
        2. Refines search queries based on JD context.
        3. Identifies industry early to stop 'Role Forcing'.
        """
        company_name = state['company_name']
        jd_context = state.get('job_description', '')
        
        print(f"AGENT: Router analyzing request for '{company_name}'...")
        
        prompt = f"""
        Analyze this company name: '{company_name}'
        User Context (JD): {jd_context if jd_context else 'No job description provided.'}
        
        TASKS:
        1. Is this a common abbreviation (like AZ, HP, BT, MS)?
        2. Based on the JD, what is the most likely company, industry, and GEOGRAPHIC LOCATION?
        3. Generate a search query that targets CURRENT ({datetime.now().year}-{datetime.now().year + 1}) interview experiences.
        4. If the company is regional (e.g., specific to India, UK, etc.), INCLUDE the location in the query to avoid acronym collisions.
        
        CRITICAL: If NO Job Description is provided, ONLY search for the company name + 'interview questions/process'.
        DO NOT add terms like 'software engineer' or 'coding' unless the industry is strictly Tech or the JD asks for it.
        
        Return ONLY a JSON:
        {{
            "is_ambiguous": boolean,
            "suggested_query": "specific search string",
            "detected_industry": "string or null",
            "detected_location": "string or null",
            "reasoning": "short explanation"
        }}
        """
        
        try:
            current_year = datetime.now().year
            response = await gemini_service.generate_json(prompt)
            state['search_query'] = response.get('suggested_query', f"{company_name} interview questions {current_year}")
            state['industry'] = response.get('detected_industry')
            state['detected_location'] = response.get('detected_location')
            state['audit_log'].append(f"ROUTER: Identified industry as '{state['industry']}'. Reasoning: {response.get('reasoning')}")
        except Exception as e:
            # Fallback
            current_year = datetime.now().year
            state['search_query'] = f"{company_name} interview process {current_year}"
            state['audit_log'].append(f"ROUTER: Fallback query generated due to AI error: {e}")
            
        return state

    async def researcher_node(self, state: AgentState) -> AgentState:
        """Dual-Search node: Captures established DNA + Recent trends"""
        company_name = state['company_name']
        current_year = datetime.now().year
        query = state.get('search_query') or f"{company_name} interview questions {current_year}"
        
        print(f"AGENT: Researcher looking for '{company_name}' using query: '{query}'...")
        
        try:
            def do_search():
                with DDGS() as ddgs:
                    # 1. Main Search
                    results = list(ddgs.text(query, max_results=8))
                    return results
            
            results = await asyncio.to_thread(do_search)
            search_results = "\n".join([f"[{'RECENT' if i >= 3 else 'GENERAL'}] {r['title']}: {r['body']}" for i, r in enumerate(results)])
            
            if not results:
                print(f"WARNING: No public info found for {state['company_name']}. Switching to Synthetic Logic.")
                state['is_synthetic'] = True
                state['confidence_score'] = 20
                state['research_data'] = "No public information available. This might be a stealth startup or private company."
                state['sources'] = []
            else:
                # ⚡ PURGE: Hard-filter generic SEO interview article domains BEFORE AI sees them
                GENERIC_ARTICLE_DOMAINS = [
                    "datacamp.com", "guru99.com", "intellipaat.com", "interviewbit.com",
                    "geeksforgeeks.org", "theysaid.io", "interviewsidekick.com",
                    "theinterviewguys.com", "guvi.in", "simplilearn.com",
                    "analyticsvidhya.com", "javatpoint.com", "edureka.co",
                    "mindmajix.com", "careerride.com", "ambitionbox.com/advice"
                ]
                purged = [r for r in results if not any(d in r.get('href', '') for d in GENERIC_ARTICLE_DOMAINS)]
                results = purged if purged else results  # fallback: keep all if purge wiped everything
                print(f"PURGE: {len(results)} sources remain after generic-article domain filter.")

                state['is_synthetic'] = False
                state['confidence_score'] = min(85, len(results) * 15)
                state['research_data'] = "\n".join([
                    f"[{'RECENT' if i >= 3 else 'GENERAL'}] {r['title']}: {r['body']}"
                    for i, r in enumerate(results)
                ])
                state['sources'] = [
                    {
                        "title": f"{'[RECENT] ' if i >= 3 else ''}{r['title']}",
                        "url": r['href'],
                        "content": r.get('body', '')[:500]
                    } for i, r in enumerate(results)
                ]
                print(f"RESEARCH: Successfully gathered intelligence ({len(results)} sources).")

        except Exception as e:
            print(f"ERROR: Researcher failed: {e}")
            state['error'] = str(e)
            state['research_data'] = "No search results found."
            state['confidence_score'] = 0
            state['sources'] = []

        return state

    async def auditor_node(self, state: AgentState) -> AgentState:
        """The Bouncer: Filters out 'Vomit' and verifies Identity vs JD"""
        research_data = state['research_data']
        company_name = state['company_name']
        jd_context = state.get('job_description', '')
        
        print("AGENT: Auditor analyzing source quality...")
        
        prompt = f"""
        Analyze these research snippets for '{company_name}'.
        User Role Context: {jd_context}
        
        DATA:
        {research_data}
        
        TASKS:
        1. Identity & Location Check: Do these results actually belong to '{company_name}' in the correct location? 
           (CRITICAL: Reject 'Moffitt Cancer Center' if the target is 'MOC Cancer Care India'!)
        2. Relevance Audit: Score each source 0-100 on how well it describes THE INTERVIEW PROCESS AT '{company_name}' SPECIFICALLY.
        3. Noise Filter: 
           - Remove product ads, unrelated news, or companies with similar-looking names.
           - CRITICAL: REJECT any source that is a generic "Top N Interview Questions" article 
             (e.g., from datacamp, guru99, intellipaat, GeeksForGeeks, simplilearn) 
             UNLESS it explicitly mentions '{company_name}' by name in the content.
           - REJECT any source about generic AI/ML/coding concepts unless '{company_name}' is a tech firm 
             AND the source explicitly discusses '{company_name}' hiring.
        
        Return a JSON with:
        {{
            "is_identity_verified": boolean,
            "is_location_matched": boolean,
            "relevant_snippets": "cleaned string of useful data — ONLY include content that specifically mentions '{company_name}'",
            "audit_trail": ["list of what was KEPT or REJECTED with specific reasons like 'Wrong Location', 'Acronym Collision', or 'Generic Article - No Company Mention'"],
            "confidence_boost": integer
        }}
        """
        
        try:
            audit_result = await gemini_service.generate_json(prompt)
            state['audited_data'] = audit_result.get('relevant_snippets', research_data)
            state['audit_log'].extend(audit_result.get('audit_trail', []))
            
            # Step 2.5: Role-Company Domain Guard (Prevent 'Role Forcing')
            domain_mismatch = False
            if jd_context:
                # Simple keyword check for mismatch profiles
                tech_role = any(tech in jd_context.lower() for tech in ["developer", "engineer", "software", "coding", "tech", "data"])
                non_tech_company = any(noise in company_name.lower() or noise in (state.get('industry') or "").lower() for noise in ["production", "creative", "marketing", "agency", "hospital", "legal", "law", "construction"])
                
                # If it's a tech role but a non-tech company, be very suspicious of generic tech interview links
                if tech_role and non_tech_company:
                    state['audit_log'].append("DOMAIN GUARD: Flagged tech-role at non-tech company. Scrutinizing generic results.")
            
            if not audit_result.get('is_identity_verified'):
                print(f"AUDITOR: FAILED IDENTITY CHECK for {company_name}")
                state['is_valid'] = False
                state['error'] = f"Identity Collision: These search results are likely for a different '{company_name}'."
            else:
                state['confidence_score'] += audit_result.get('confidence_boost', 0)
        except:
            state['audited_data'] = research_data # Fallback
            
        return state

    async def architect_node(self, state: AgentState):
        """Generates the final profile using purified data"""
        company_name = state['company_name']
        audited_data = state['audited_data']
        jd_context = state.get('job_description', '')
        industry = state.get('industry', 'General Industry')
        
        print(f"AGENT: Architect building dynamic profile for {company_name} ({industry})...")
        
        input_data = f"COMPANY: {company_name}\nINDUSTRY: {industry}\n\nDATA:\n{audited_data}"
        if jd_context:
            input_data += f"\n\nROLE CONTEXT: {jd_context}"

        prompt = f"""
        Create a detailed Interview Intelligence Profile for '{company_name}'.
        
        {input_data}
        
        DYNAMIC ROUNDS POLICY:
        Instead of a fixed set of rounds, identify the 3-4 MOST LIKELY rounds for this specific industry.
        - For Healthcare: Focus on Clinical rounds, Patient Management, and Behavioral.
        - For Finance: Focus on Quantitative, Market Knowledge, and Culture.
        - For Tech: Focus on Coding, System Design, and leadership.
        
        NEGATIVE EVIDENCE POLICY:
        If the research data shows the company primarily hires for non-tech roles (Administrative, Clinical, Legal, etc.) and you found NO SPECIFIC evidence of tech hiring, you MUST:
        1. State this clearly in 'interview_style'.
        2. DO NOT include tech rounds unless the JD explicitly asks for it.
        3. Replace Tech rounds with 'Industry Standard [Role Type] Assessment'.

        STRICT BIAS GUARD: 
        1. If NO Job Description is provided AND the Industry is non-Tech (Healthcare, Legal, etc.), DO NOT include 'Coding', 'LeetCode', or 'System Design (Software)' rounds unless the search data explicitly mentions them.
        2. Instead, use domain-appropriate rounds like 'Clinical Case Study', 'Regulatory Compliance', or 'Practical Skills Test'.
        3. If research is sparse, use 'Industry Standard [Domain] Round'.

        SCHEMA:
        {{
            "name": "string",
            "industry": "string",
            "size": "string",
            "interview_style": "string",
            "difficulty_level": "string",
            "cultural_values": ["list"],
            "interview_rounds": {{
                "Round Name 1": {{ "focus": "string", "common_topics": ["list"], "style": "string", "tips": "string" }},
                "Round Name 2": {{ "focus": "string", "common_questions": ["list"], "style": "string" }},
                "Round Name 3": {{ "focus": "string", "common_topics": ["list"], "style": "string" }}
            }},
            "red_flags": ["list"],
            "average_process_duration": "string",
            "interview_count": "string",
            "role_company_alignment": "Explain how the role fits this industry in 2 sentences."
        }}
        """
        
        profile = await gemini_service.generate_json(prompt)
        state['generated_profile'] = profile
        state['iterations'] += 1
        return state

    async def critic_node(self, state: AgentState):
        """Verifies profile accuracy and schema alignment"""
        profile = state['generated_profile']
        industry = state.get('industry', 'Unknown')
        
        print("AGENT: Critic evaluating profile integrity...")
        
        prompt = f"""
        Review this generated Interview Profile for correctness.
        Industry Context: {industry}
        
        PROFILE:
        {json.dumps(profile, indent=2)}
        
        CHECKLIST:
        1. Hallucination Check: Is it claiming tech rounds for a non-tech company?
        2. Industry Match: Does the interview style match '{industry}'?
        3. Grounding: Is this derived from the research data or a generic guess?
        4. Cross-Continental Hallucination: Is it confused between companies with similar names in different countries? (e.g., USA vs India).
        
        FATAL REJECTION RULE: If the company is in a non-tech industry (Healthcare, Legal, etc.) and you see 'LeetCode', 'System Design (Distributed)', or 'Coding Test' in the rounds without specific evidence in the research, REJECT with 'ROLE FORCING DETECTED'.
        
        If perfect, return 'APPROVED'. Else return corrections.
        """
        
        critique = await gemini_service.generate_text(prompt)
        
        if "APPROVED" in critique.upper():
            state['is_valid'] = True
        else:
            print(f"CRITIC: Profile rejected. Reason: {critique}")
            state['is_valid'] = False
            state['audit_log'].append(f"CRITIC REJECTION: {critique}")
            
        return state

    def create_workflow(self):
        workflow = StateGraph(AgentState)

        # Add Nodes
        workflow.add_node("router", self.router_node)
        workflow.add_node("researcher", self.researcher_node)
        workflow.add_node("auditor", self.auditor_node)
        workflow.add_node("architect", self.architect_node)
        workflow.add_node("critic", self.critic_node)

        # Define Edges
        workflow.set_entry_point("router")
        workflow.add_edge("router", "researcher")
        workflow.add_edge("researcher", "auditor")
        workflow.add_edge("auditor", "architect")
        workflow.add_edge("architect", "critic")

        # Conditional Edge: If not valid and under 2 iterations, go back to architect
        def should_continue(state: AgentState):
            if state['is_valid'] or state['iterations'] >= 2:
                return END
            return "architect"

        workflow.add_conditional_edges("critic", should_continue)

        return workflow.compile()

    async def get_intelligence(self, company_name: str, job_description: str = None) -> Dict[str, Any]:
        """Entry point for the backend to get company intelligence"""
        # 1. First check the curated database
        intel_service = get_company_intelligence()
        profile = intel_service.get_company_profile(company_name)
        
        if profile:
            return profile

        # 2. Check the Agentic Discovery Memory (discoveries.json) with STRICT Matching
        print("INFO: Checking Discovery Memory...")
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            discoveries_path = os.path.join(base_dir, "data", "discoveries.json")
            if os.path.exists(discoveries_path):
                with open(discoveries_path, 'r', encoding='utf-8') as f:
                    discoveries = json.load(f)
                    
                    # Instead of fuzzy matching everything, use the tiered logic or 98% threshold
                    for entry in discoveries:
                        stored_name = entry.get('company_name', '').lower()
                        if stored_name == company_name.lower():
                            print(f"FOUND: Exact match in discoveries memory for '{company_name}'")
                            return entry.get('interview_intelligence_profile', entry)
                            
                    # If not exact, try a VERY high threshold fuzzy match
                    discovery_names = [d.get('company_name', '') for d in discoveries]
                    if discovery_names:
                        match = process.extractOne(company_name, discovery_names, scorer=fuzz.WRatio)
                        if match and match[1] >= 98: # Extreme threshold to prevent collisions
                             matched_name = match[0]
                             for d in discoveries:
                                if d.get('company_name') == matched_name:
                                    print(f"FOUND: High-precision discovery match '{company_name}' -> '{matched_name}'")
                                    return d.get('interview_intelligence_profile', d)
        except Exception as e:
            print(f"WARNING: Memory lookup failed: {e}")

        # 3. If not found, trigger the Agentic Workflow
        print(f"INFO: {company_name} not found in memory. Starting Agentic Discovery...")
        
        app = self.create_workflow()
        initial_state: AgentState = {
            "company_name": company_name,
            "industry": None,
            "job_description": job_description,
            "research_data": None,
            "is_synthetic": False,
            "confidence_score": 0,
            "generated_profile": None,
            "is_valid": False,
            "iterations": 0,
            "sources": [],
            "search_query": None,
            "audited_data": None,
            "audit_log": [],
            "error": None
        }
        
        final_state = await app.ainvoke(initial_state)
        print(f"INFO: Agent Workflow Complete. Profile generated: {final_state.get('generated_profile') is not None}")
        
        if final_state.get('generated_profile'):
            profile = final_state['generated_profile']
            # Inject score and sources
            profile['confidence_score'] = final_state.get('confidence_score', 0)
            profile['is_synthetic'] = final_state.get('is_synthetic', False)
            profile['sources'] = final_state.get('sources', [])
            
            # Developer-Only Audit Logs (Not for end-users)
            new_entry = {
                "company_name": final_state.get('company_name') or company_name,
                "interview_intelligence_profile": profile,
                "audit_log": final_state.get('audit_log', [])
            }
            try:
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                data_dir = os.path.join(base_dir, "data")
                discoveries_path = os.path.join(data_dir, "discoveries.json")
                
                print(f"LOG: Saving discovery to: {discoveries_path}")
                
                discoveries = []
                if os.path.exists(discoveries_path):
                    with open(discoveries_path, 'r', encoding='utf-8') as f:
                        discoveries = json.load(f)
                
                # Check if already discovered (case-insensitive)
                is_duplicate = False
                for d in discoveries:
                    existing_name = d.get('company_name')
                    if existing_name and existing_name.lower() == new_entry['company_name'].lower():
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    # SAFETY CHECK: Only save to global memory if it's VALIDATED and NOT synthetic
                    if final_state.get('is_valid') and not final_state.get('is_synthetic'):
                        discoveries.append(new_entry)
                        with open(discoveries_path, 'w', encoding='utf-8') as f:
                            json.dump(discoveries, f, indent=4)
                        print(f"SUCCESS: New Discovery Saved: {new_entry['company_name']} added to discoveries.json")
                    else:
                        print(f"INFO: {new_entry['company_name']} is a Synthetic (Stealth) profile. Not saving to global memory for data integrity.")
            except Exception as e:
                print(f"ERROR: Could not save discovery: {e}")
                
            return profile
        
        return {"error": final_state.get('error', "Agent failed to generate intelligence.")}

# Singleton instance
_intelligence_service = None

def get_intelligence_service() -> IntelligenceService:
    global _intelligence_service
    if _intelligence_service is None:
        _intelligence_service = IntelligenceService()
    return _intelligence_service
