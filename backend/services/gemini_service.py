from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = "gemini-2.0-flash"

    async def analyze_resume(self, resume_text: str, jd: str = None):
        """Premium Feature: Analyzes resume against a JD and provides ATS score + Gap Analysis."""
        prompt = f"""
        You are a Senior Technical Recruiter and ATS Optimization Expert.
        
        RESUME:
        {resume_text}
        
        {f"JOB DESCRIPTION: {jd}" if jd else "General Industry Standards"}
        
        TASK:
        1. Calculate an ATS Score (0-100).
        2. Identify Key Strengths (3 points).
        3. Identify Weaknesses/Gaps (3 points).
        4. Provide actionable tips to improve the resume for this specific role.
        
        Return the result in JSON format:
        {{
            "ats_score": 85,
            "strengths": [],
            "weaknesses": [],
            "tips": []
        }}
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        return response.text

    async def generate_interview_question(self, role: str, sub_role: str, difficulty: int, company: str = None, round_name: str = "Technical", is_panel: bool = False, jd: str = None, resume_text: str = None, chat_history: list = [], current_time: str = None, interviewer_name: str = "Adinath"):
        """Generates a contextual interview question with optional Panel and Pressure simulation."""
        
        difficulty_map = {1: "Junior", 2: "Mid-level", 3: "Senior/Lead"}
        level = difficulty_map.get(difficulty, "Junior")

        # Point 1: Panel Interview Logic
        panel_instruction = f"""
        ACT AS A PANEL: You represent multiple interviewers. 
        - Interviewer A ({interviewer_name}): Lead Recruiter, focused on background.
        - Interviewer B (Arav): Technical Architect, focused on efficiency.
        Alternate between these two personas. Mention who is asking in the text (e.g., '[{interviewer_name}]: ...').
        """ if is_panel else ""

        system_prompt = f"""
        You are {interviewer_name.upper()}, a Simulation Assistant designed to mimic high-level professional interviewers.
        The name {interviewer_name} signifies eternal knowledge and primal wisdom.
        Current Date/Time for context: {current_time if current_time else "Unknown"}
        
        CRITICAL IDENTITY INSTRUCTIONS:
        - NEVER claim to be an actual employee of {company if company else "any firm"}.
        - ALWAYS frame yourself as a simulation. Example: "I am {interviewer_name}, simulating a {round_name} interview round based on {company if company else "industry"} standards."
        - Avoid phrases like "I work at Google" or "I am a recruiter at Amazon." Use "I represent the simulation for..." or "I am your AI interviewer for this {company if company else ""} practice session."
        
        You're simulating the {round_name} round for {sub_role} ({role} category) at a {level} level.
        
        {panel_instruction}
        
        {f"STRICT SIMULATION PARAMETERS: Mimic {company}'s specific culture and values." if company else ""}
        
        PROTOCOL:
        - Turn 0 (Start): GREET the candidate warmly but professionally. Greet them based on the current time. Introduce yourself as {interviewer_name} and EXPLICITLY state this is an AI Simulation. If in Panel mode, introduce your co-simulation persona (e.g., Arav). Ask for a brief intro.
        - Turn 1 (After Intro): Simple acknowledgment of their background. Mention something specific from their intro or resume.
        - Turn 2+: Start the core simulated technical/behavioral interview.
        
        { "PRESSURE MODE: Ask a follow-up optimization question and challenge the candidate's last answer." if len(chat_history) > 6 else "" }

        YOUR GOAL:
        - Ask ONE question at a time.
        - BE CREATIVE & NON-STANDARD in core questions. 
        - NO SUGARCOATING performance later, but maintain simulation boundaries.
        - Tie questions to projects in resume if provided: {resume_text[:300] if resume_text else "None"}
        """

        # Convert simple transcript list back to Gemini content objects
        contents = []
        for i, msg in enumerate(chat_history):
            # i=0: assistant(model), i=1: user, i=2: assistant(model), etc.
            role_type = "model" if i % 2 == 0 else "user"
            contents.append(types.Content(role=role_type, parts=[types.Part(text=msg)]))

        # Add the instruction for the next turn
        instruction = "Please ask the first question." if not contents else "Please ask the next follow-up question based on the conversation."
        contents.append(types.Content(role="user", parts=[types.Part(text=instruction)]))
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt
            )
        )
        
        return response.text

    async def evaluate_answer(self, question: str, answer: str, role: str, company: str = None):
        """Evaluates with Point 2: Behavioral Vibe & Tone Analysis included."""
        prompt = f"""
        Role: {role} at {company if company else "Tech Firm"}
        Question: {question}
        User Answer: {answer}
        
        TASK:
        1. Evaluate technical accuracy.
        2. VIBE ANALYSIS: Analyze tone, confidence, and 'um/uh' hesitation conceptually from text.
        3. ASSERTIVENESS: Did they sound like a leader or a subordinate?
        
        RATING CRITERIA (1-10):
        10: Mind-blowing, unique, and technically perfect.
        7-8: Solid, industry standard.
        5-6: Needs significant work, too generic.
        <4: Reject.
        
        FEEDBACK STYLE:
        - NO SUGARCOATING. Be direct. If the answer was bad, say why clearly.
        
        Return JSON:
        {{
            "score": float,
            "feedback": "string",
            "vibe_analysis": {{
                "confidence_score": 0-10,
                "hesitation_level": "High/Med/Low",
                "assertiveness": "string feedback"
            }},
            "can_proceed": boolean
        }}
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        return response.text

    async def generate_learning_roadmap(self, role: str, sub_role: str, failed_topics: list):
        """Point 3: Generates a 7-Day Curriculum after a failed round."""
        prompt = f"""
        The candidate failed their {sub_role} interview in these topics: {failed_topics}.
        Generate a strict 7-Day Learning Roadmap.
        
        Day 1-2: Fundamentals of failed concepts.
        Day 3-4: Advanced implementation and trade-offs.
        Day 5: Real-world scenario practicing.
        Day 6: Mock simulation prep.
        Day 7: Final review.
        
        Return JSON:
        {{
            "focus_areas": [],
            "curriculum": {{"Day 1": "..."}},
            "resources": []
        }}
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        return response.text

gemini_service = GeminiService()
