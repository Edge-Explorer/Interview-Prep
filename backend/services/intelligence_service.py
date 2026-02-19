# AUTHOR: Karan Shelar (GitHub: Edge-Explorer)
# PROJECT: InterviewAI - Advanced Intelligence System
# ROLE: Lead Architect & AI Engineer
import os
import json
import asyncio
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

# Placeholder for Local Llama Loading
# We will implement this safely as a lazy-loader
try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from peft import PeftModel
    HAS_LOCAL_ML = True
except ImportError:
    HAS_LOCAL_ML = False

class AgentState(TypedDict):
    company_name: str
    industry: Optional[str]
    job_description: Optional[str]        # NEW: Context from user
    research_data: Optional[str]
    is_synthetic: bool                    # NEW: Tracker for non-public info
    confidence_score: int                 # NEW: 0-100 score of data reliability
    generated_profile: Optional[Dict[str, Any]]
    is_valid: bool
    iterations: int
    sources: List[Dict[str, str]]        
    audited_data: Optional[str]           # NEW: Cleaned data for the Architect
    audit_log: List[str]                  # NEW: Developer notes on filtering
    error: Optional[str]

class IntelligenceService:
    def __init__(self):
        self.critic_llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.getenv("GEMINI_API_KEY"))
        self.model = None
        self.tokenizer = None
        self.local_model_path = os.path.join(os.path.dirname(__file__), "..", "interview_ai_model")
        self.base_model_id = "unsloth/llama-3-8b-instruct-bnb-4bit" # This might need to be changed based on user hardware

    def _load_local_model(self):
        """Lazy loader for the fine-tuned Llama model"""
        if self.model is not None:
            return
        
        if not HAS_LOCAL_ML:
            print("WARNING: Local ML libraries (torch, transformers, peft) not found. Skipping local model load.")
            return

        print("INFO: Loading Fine-Tuned Llama-3 Model... This may take a minute.")
        try:
            # Note: This is a simplified loading logic. 
            # In a real local environment, user might need specific torch versions.
            self.tokenizer = AutoTokenizer.from_pretrained(self.local_model_path)
            
            # Load base model (4-bit if possible)
            # For simplicity in this first draft, we assume the user has enough RAM/VRAM
            # If they used Unsloth, they likely want 4-bit.
            base_model = AutoModelForCausalLM.from_pretrained(
                self.base_model_id,
                torch_dtype=torch.float16,
                device_map="auto"
            )
            
            # Load LoRA Adapters
            self.model = PeftModel.from_pretrained(base_model, self.local_model_path)
            print("SUCCESS: Fine-Tuned Model Loaded successfully!")
        except Exception as e:
            print(f"ERROR: Error loading local model: {e}")
            self.model = None

    async def researcher_node(self, state: AgentState) -> AgentState:
        """Dual-Search node: Captures established DNA + Recent 2026 trends"""
        print(f"STATUS: Stage 1/3 - Researching {state['company_name']}...")
        print(f"RESEARCH: Scouring professional sources with Temporal Priority...")
        try:
            # Dynamic year for "Evergreen Freshness"
            from datetime import datetime
            current_year = datetime.now().year
            prev_year = current_year - 1
            
            # Plan: Two queries to balance "Established History" with "Fresh Trends"
            dna_query = f'"{state["company_name"]}" (interview process OR company culture OR tech stack)'
            trends_query = f'"{state["company_name"]}" interview experience {prev_year} {current_year}'
            
            def do_search():
                with DDGS() as ddgs:
                    # 1. Get broader DNA (no strict timelimit)
                    dna_results = [r for r in ddgs.text(dna_query, max_results=3)]
                    # 2. Get cutting-edge trends (strictly last year to catch 2025/2026)
                    trend_results = [r for r in ddgs.text(trends_query, max_results=3, timelimit='y')]
                    
                    return dna_results + trend_results
            
            results = await asyncio.to_thread(do_search)
            search_results = "\n".join([f"[{'RECENT' if i >= 3 else 'GENERAL'}] {r['title']}: {r['body']}" for i, r in enumerate(results)])
            
            if not results:
                print(f"WARNING: No public info found for {state['company_name']}. Switching to Synthetic Logic.")
                state['is_synthetic'] = True
                state['confidence_score'] = 20
                state['research_data'] = "No public information available. This might be a stealth startup or private company."
                state['sources'] = []
            else:
                state['is_synthetic'] = False
                state['confidence_score'] = min(85, len(results) * 15) # Boost base confidence for fresh data
                state['research_data'] = search_results
                # Capture sources with temporal tagging
                state['sources'] = [{"title": f"{'[RECENT] ' if i >= 3 else ''}{r['title']}", "url": r['href']} for i, r in enumerate(results)]
                print(f"RESEARCH: Successfully gathered intelligence blocks (DNA + Recent Trends).")
        except Exception as e:
            state['error'] = f"Research failed: {str(e)}"
            state['research_data'] = "No search results found."
            state['confidence_score'] = 0
            state['sources'] = []
        return state

    async def auditor_node(self, state: AgentState) -> AgentState:
        """The Bouncer: Filters out 'Vomit' and verifies Identity vs JD"""
        print(f"STATUS: Stage 1.5 - Auditing Intelligence for {state['company_name']}...")
        
        raw_results = state.get('sources', [])
        jd_context = (state.get('job_description') or "").lower()
        company_name = state['company_name'].lower()
        
        # Identity Killers (Noise words that signal irrelevant results)
        noise_keywords = ["vastu", "astrology", "ncert", "bihar board", "class 7", "class 8", "class 9", "religious", "bhajan", "playlist"]
        
        clean_sources = []
        audit_trail = []
        
        # Step 1: Filter Junk
        for source in raw_results:
            title = source['title'].lower()
            url = source['url'].lower()
            
            # Check for Noise
            is_noise = any(noise in title or noise in url for noise in noise_keywords)
            if is_noise:
                audit_trail.append(f"REJECTED: '{source['title']}' identified as noise/irrelevant.")
                continue
                
            # Step 2: Contextual Match (Identity Audit)
            relevance_score = 0
            if jd_context:
                # Check for tech keywords in title/url if JD is tech-heavy
                tech_indicators = ["python", "react", "java", "developer", "engineer", "data", "qa", "test", "sde", "coding", "software", "tech"]
                if any(tech in jd_context for tech in tech_indicators):
                    if any(tech in title or tech in url for tech in tech_indicators):
                        relevance_score += 50
            
            # Domain Trust (Auto-boost for professional sites)
            trust_domains = ["linkedin.com", "glassdoor.", "ambitionbox.com", "levels.fyi", "cutshort.io", "indeed.", "github.com", "ycombinator.com"]
            if any(domain in url for domain in trust_domains):
                relevance_score += 40
                
            # Keep if it has at least some relevance or is from a trusted domain
            if relevance_score >= 30 or not jd_context:
                clean_sources.append(source)
                audit_trail.append(f"ACCEPTED: '{source['title']}' (Score: {relevance_score})")
            else:
                audit_trail.append(f"REJECTED: '{source['title']}' failed relevance audit (Score: {relevance_score})")

        # Deduplicate
        seen_urls = set()
        unique_sources = []
        for s in clean_sources:
            if s['url'] not in seen_urls:
                unique_sources.append(s)
                seen_urls.add(s['url'])

        # Step 3: Identity Verification (The Stealth-Mode Pivot)
        if not unique_sources:
            print(f"CRITICAL: Auditor found 0 relevant links out of {len(raw_results)}. Identity Mismatch suspected.")
            state['is_synthetic'] = True
            state['confidence_score'] = 15
            state['audited_data'] = "No professionally relevant data found. The company might be a stealth startup or the name might collide with non-professional entities."
            state['sources'] = [] # Clear the trash sources
        else:
            state['sources'] = unique_sources
            state['audited_data'] = f"AUDITED DATA (Trusted Sources Only):\n" + "\n".join([f"- {s['title']}" for s in unique_sources])
            state['confidence_score'] = min(90, len(unique_sources) * 20)
            print(f"AUDITOR: Successfully filtered {len(raw_results)} -> {len(unique_sources)} high-grade sources.")

        state['audit_log'] = audit_trail
        return state

    async def architect_node(self, state: AgentState) -> AgentState:
        """Use the Fine-Tuned Brain (Llama-3) to generate the profile"""
        print(f"STATUS: Stage 2/3 - Architecting DNA for {state['company_name']}...")
        print(f"ARCHITECT: Synthesizing data into interview patterns...")
        
        instruction = f"Generate a professional interview intelligence profile for {state['company_name']}."
        input_data = f"Research Data (Audited): {state.get('audited_data', state['research_data'])[:2000]}"
        if state.get('job_description'):
            input_data += f"\n\nContext from Job Description provided by user: {state['job_description']}"
            
        if state.get('is_synthetic'):
             input_data += "\n\nNOTE: Since no public info was found, synthesize a high-fidelity profile based EXCLUSIVELY on industry standards for the role described in the JD. Do not hallucinate history."

        input_data += "\n\nHALLUCINATION POLICY: If specific information (like CEO, recent news, or exact round names) is not in the research data, DO NOT MAKE IT UP. Instead, return 'Data not available in public records' for that field."

        # Alpaca prompt template used during fine-tuning
        prompt = f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{instruction}

### Input:
{input_data}

### Response:
"""

        # If model is loaded, use the local "Brain"
        if self.model is not None:
            try:
                print("INFO: Brain is thinking (Local Llama-3)...")
                inputs = self.tokenizer([prompt], return_tensors="pt").to("cuda")
                
                # Using generation params similar to Colab
                outputs = await asyncio.to_thread(
                    self.model.generate,
                    **inputs, 
                    max_new_tokens=1000,
                    use_cache=True
                )
                
                decoded = self.tokenizer.batch_decode(outputs)
                response_text = decoded[0].split("### Response:")[1].strip()
                
                # Parse the generated text (it should be a JSON-like structure or matches our schema)
                # Note: Our model was trained to output structured text that we can convert to JSON
                state['generated_profile'] = self._parse_to_schema(response_text, state['company_name'])
                return state
            except Exception as e:
                print(f"WARNING: Local inference failed: {e}. Falling back to Gemini Architect.")

        # Fallback to Gemini if local model is unavailable or fails
        fallback_prompt = f"{prompt}\n(Note: Please output valid JSON matching our schema)"
        try:
            response = await asyncio.to_thread(
                gemini_service.client.models.generate_content,
                model="gemini-2.0-flash",
                contents=fallback_prompt
            )
            json_str = response.text
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0].strip()
            state['generated_profile'] = json.loads(json_str)
        except Exception as e:
            print(f"ERROR: Architect generation failed: {e}")
            state['error'] = "Failed to parse architect output"
            
        return state

    def _parse_to_schema(self, text: str, company_name: str) -> Dict[str, Any]:
        """Convert the fine-tuned model's text output into our system's JSON schema"""
        # This is a helper to ensure the Llama output matches the project's exact JSON format
        # If the model was trained on the JSON files, it will likely output JSON.
        try:
            # Try parsing as JSON first
            return json.loads(text)
        except:
            # If it's structured text, we have a problem we'll fix later with a regex or more training
            # For now, we assume it's JSON because we trained on training_data.json
            return {"name": company_name, "raw_data": text}

    async def critic_node(self, state: AgentState) -> AgentState:
        """Review the profile for quality and consistency"""
        print(f"STATUS: Stage 3/3 - Final Audit for {state['company_name']}...")
        print("CRITIC: Validating company profile for accuracy...")
        
        profile = state.get('generated_profile')
        if not profile:
            state['is_valid'] = False
            return state

        # Use Gemini to critique the structural output against the research data
        critique_prompt = f"""
        Review this generated company profile for {state['company_name']}.
        
        CRITICAL TASK: Compare the profile against the RAW RESEARCH DATA below.
        If the profile contains SPECIFIC facts (dates, names, news) that are NOT in the research data, it is a HALLUCINATION.
        
        RAW RESEARCH DATA:
        {state['research_data'][:2000]}
        
        GENERATED PROFILE:
        {json.dumps(profile, indent=2)}
        
        If it's grounded in the research and matches our schema, return ONLY the word 'APPROVED'.
        If it has hallucinations or errors, return a short list of corrections.
        """
        response = await asyncio.to_thread(self.critic_llm.invoke, critique_prompt)
        
        if "APPROVED" in response.content:
            state['is_valid'] = True
            state['confidence_score'] = min(100, state['confidence_score'] + 25)
        else:
            state['is_valid'] = False
            state['iterations'] += 1
            state['confidence_score'] = max(0, state['confidence_score'] - 20)
            print(f"ERROR: Critic Feedback: {response.content}")
            
        return state

    def create_workflow(self):
        """Assemble the LangGraph nodes"""
        workflow = StateGraph(AgentState)

        # Add Nodes
        workflow.add_node("researcher", self.researcher_node)
        workflow.add_node("auditor", self.auditor_node)
        workflow.add_node("architect", self.architect_node)
        workflow.add_node("critic", self.critic_node)

        # Define Edges
        workflow.set_entry_point("researcher")
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

        # 2. Check the Agentic Discovery Memory (discoveries.json) with FUZZY MATCHING
        print("INFO: Checking Discovery Memory...")
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            discoveries_path = os.path.join(base_dir, "data", "discoveries.json")
            if os.path.exists(discoveries_path):
                with open(discoveries_path, 'r', encoding='utf-8') as f:
                    discoveries = json.load(f)
                    
                    # Fuzzy match against discovery names
                    # INCREASED THRESHOLD: 95% ensures 'Shastra' and 'Idolize' (both ending in Solutions) don't collide
                    discovery_names = [d.get('company_name', '') for d in discoveries]
                    match = process.extractOne(company_name, discovery_names, scorer=fuzz.WRatio)
                    
                    if match and match[1] >= 95:  # Strict 95% threshold to avoid "Solutions" collisions
                        matched_name = match[0]
                        print(f"FOUND: High-confidence match '{company_name}' to '{matched_name}' (Score: {match[1]:.1f})")
                        for d in discoveries:
                            if d.get('company_name') == matched_name:
                                return d.get('interview_intelligence_profile', d)
                    else:
                        print(f"INFO: No high-confidence match found (Top score: {match[1] if match else 0:.1f}). Proceeding with fresh discovery.")
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
                    # SAFETY CHECK: Only save to global memory if it's NOT synthetic (verified web data)
                    if not final_state.get('is_synthetic'):
                        discoveries.append(new_entry)
                        with open(discoveries_path, 'w', encoding='utf-8') as f:
                            json.dump(discoveries, f, indent=4)
                        print(f"SUCCESS: New Discovery Saved: {new_entry['company_name']} added to discoveries.json")
                    else:
                        print(f"INFO: {new_entry['company_name']} is a Synthetic (Stealth) profile. Not saving to global memory for data integrity.")
                else:
                    print(f"INFO: {new_entry['company_name']} already exists in discovery memory.")
            except Exception as e:
                print(f"WARNING: Failed to save discovery: {e}")
            
            return profile

# Singleton instance
_intelligence_service = None

def get_intelligence_service() -> IntelligenceService:
    global _intelligence_service
    if _intelligence_service is None:
        _intelligence_service = IntelligenceService()
    return _intelligence_service
