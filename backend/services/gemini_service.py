import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash')

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
        response = self.model.generate_content(prompt)
        # Note: In production we'd parse this JSON properly
        return response.text

    async def generate_interview_question(self, role: str, sub_role: str, difficulty: int, company: str = None, round_name: str = "Technical", is_panel: bool = False, jd: str = None, resume_text: str = None, chat_history: list = []):
        """Generates a contextual interview question with optional Panel and Pressure simulation."""
        
        difficulty_map = {1: "Junior", 2: "Mid-level", 3: "Senior/Lead"}
        level = difficulty_map.get(difficulty, "Junior")

        # Point 1: Panel Interview Logic
        panel_instruction = """
        ACT AS A PANEL: You represent multiple interviewers. 
        - Interviewer A (Project Lead): Strict, focuses on implementation.
        - Interviewer B (System Architect): Skeptical, asks 'What if?' and about scalability.
        Alternate between these two personas. Mention who is asking in the text (e.g., '[Lead]: ...').
        """ if is_panel else ""

        system_prompt = f"""
        You are an expert professional interviewer at {company if company else "a top-tier firm"}.
        You're conducting the {round_name} round for {sub_role} ({role} category) at a {level} level.
        
        {panel_instruction}
        
        {f"STRICT INSTRUCTIONS: Follow {company}'s specific culture and values." if company else ""}
        
        { "PRESSURE MODE: Ask a follow-up optimization question. Limit the candidate's thinking time conceptually." if len(chat_history) > 4 else "" }

        YOUR GOAL:
        - Ask ONE question at a time.
        - BE CREATIVE & NON-STANDARD. No generic questions. 
        - NO SUGARCOATING. Be direct.
        """

        # Prepare chat history for Gemini
        # (Converting our DB JSON format to Gemini format)
        contents = [{"role": "user" if i % 2 == 0 else "model", "parts": [m]} for i, m in enumerate(chat_history)]
        
        # Add the system prompt/instruction
        # Starting the chat
        chat = self.model.start_chat(history=contents)
        response = chat.send_message(f"Assistant: Please ask the first or next question for the {sub_role} interview.")
        
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
        response = self.model.generate_content(prompt)
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
        response = self.model.generate_content(prompt)
        return response.text

gemini_service = GeminiService()
