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
    generated_profile: Optional[Dict[str, Any]]
    is_valid: bool
    iterations: int
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
        """Search engine node to find facts about unknown companies"""
        print(f"RESEARCH: Finding information on {state['company_name']}...")
        try:
            query = f"{state['company_name']} company overview industry products culture interview process"
            def do_search():
                with DDGS() as ddgs:
                    return [r for r in ddgs.text(query, max_results=5)]
            
            results = await asyncio.to_thread(do_search)
            search_results = "\n".join([f"{r['title']}: {r['body']}" for r in results])
            
            if not results:
                print(f"WARNING: No public info found for {state['company_name']}. Switching to Synthetic Logic.")
                state['is_synthetic'] = True
                state['research_data'] = "No public information available. This might be a stealth startup or private company."
            else:
                state['is_synthetic'] = False
                state['research_data'] = search_results
        except Exception as e:
            state['error'] = f"Research failed: {str(e)}"
            state['research_data'] = "No search results found."
        return state

    async def architect_node(self, state: AgentState) -> AgentState:
        """Use the Fine-Tuned Brain (Llama-3) to generate the profile"""
        print(f"ARCHITECT: Structuring intelligence for {state['company_name']}...")
        
        instruction = f"Generate a professional interview intelligence profile for {state['company_name']}."
        input_data = f"Research Data found: {state['research_data'][:2000]}"
        if state.get('job_description'):
            input_data += f"\n\nContext from Job Description provided by user: {state['job_description']}"
            
        if state.get('is_synthetic'):
             input_data += "\n\nNOTE: Since no public info was found, synthesize a high-fidelity profile based EXCLUSIVELY on industry standards for the role described in the JD. Do not hallucinate history."

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
        print("CRITIC: Validating company profile...")
        
        profile = state.get('generated_profile')
        if not profile:
            state['is_valid'] = False
            return state

        # Use Gemini to critique the structural output
        critique_prompt = f"""
        Review this generated company profile for {state['company_name']}.
        Ensure it matches industry reality and our schema.
        
        PROFILE:
        {json.dumps(profile, indent=2)}
        
        If it's good, return ONLY the word 'APPROVED'.
        If it has errors, return a short list of corrections.
        """
        response = await asyncio.to_thread(self.critic_llm.invoke, critique_prompt)
        
        if "APPROVED" in response.content:
            state['is_valid'] = True
        else:
            state['is_valid'] = False
            state['iterations'] += 1
            print(f"ERROR: Critic Feedback: {response.content}")
            
        return state

    def create_workflow(self):
        """Assemble the LangGraph nodes"""
        workflow = StateGraph(AgentState)

        # Add Nodes
        workflow.add_node("researcher", self.researcher_node)
        workflow.add_node("architect", self.architect_node)
        workflow.add_node("critic", self.critic_node)

        # Define Edges
        workflow.set_entry_point("researcher")
        workflow.add_edge("researcher", "architect")
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
            print(f"FOUND: {company_name} in Curated Database!")
            return profile

        # 2. Check the Agentic Discovery Memory (discoveries.json)
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            discoveries_path = os.path.join(base_dir, "data", "discoveries.json")
            if os.path.exists(discoveries_path):
                with open(discoveries_path, 'r', encoding='utf-8') as f:
                    discoveries = json.load(f)
                    # Check for a match (fuzzy match here would be even better)
                    for d in discoveries:
                        if d.get('company_name', '').lower() == company_name.lower():
                            print(f"FOUND: {company_name} in Agentic Discovery Memory!")
                            # Return the profile part (discovery.json has a slightly different wrapper)
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
            "generated_profile": None,
            "is_valid": False,
            "iterations": 0,
            "error": None
        }
        
        final_state = await app.ainvoke(initial_state)
        print(f"INFO: Agent Workflow Complete. Profile generated: {final_state.get('generated_profile') is not None}")
        
        if final_state.get('generated_profile'):
            profile = final_state['generated_profile']
            # Save discovery to a file for human review later (Infinite Learning Loop)
            try:
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                data_dir = os.path.join(base_dir, "data")
                discoveries_path = os.path.join(data_dir, "discoveries.json")
                
                print(f"LOG: Saving discovery to: {discoveries_path}")
                
                discoveries = []
                if os.path.exists(discoveries_path):
                    with open(discoveries_path, 'r', encoding='utf-8') as f:
                        discoveries = json.load(f)
                
                # Normalize the entry to our standard discovery format
                # We want: { "company_name": "...", "interview_intelligence_profile": { ... } }
                name_to_use = profile.get('company_name') or profile.get('name') or company_name
                
                new_entry = {
                    "company_name": name_to_use,
                    "interview_intelligence_profile": profile
                }

                # Check if already discovered (case-insensitive)
                is_duplicate = False
                for d in discoveries:
                    existing_name = d.get('company_name')
                    if not existing_name and 'name' in d: # Fallback for old/direct profiles
                        existing_name = d.get('name')
                    
                    if existing_name and existing_name.lower() == name_to_use.lower():
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    discoveries.append(new_entry)
                    with open(discoveries_path, 'w', encoding='utf-8') as f:
                        json.dump(discoveries, f, indent=4)
                    print(f"SUCCESS: New Discovery Saved: {name_to_use} added to discoveries.json")
                else:
                    print(f"INFO: {name_to_use} already exists in discovery memory.")
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
