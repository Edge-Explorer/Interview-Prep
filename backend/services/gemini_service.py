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

    async def generate_interview_question(self, role: str, sub_role: str, difficulty: int, company: str = None, round_name: str = "Technical", jd: str = None, resume_text: str = None, chat_history: list = []):
        """Generates a contextual interview question based on role, difficulty, company, round, resume, and history."""
        
        difficulty_map = {1: "Junior", 2: "Mid-level", 3: "Senior/Lead"}
        level = difficulty_map.get(difficulty, "Junior")

        system_prompt = f"""
        You are an expert professional interviewer at {company if company else "a top-tier firm"}.
        You are currently conducting the {round_name} round for the position of {sub_role} ({role} category) at a {level} level.
        
        {f"STRICT INSTRUCTIONS: Follow {company}'s specific interview style, culture, and core values (e.g., Amazon's Leadership Principles, Google's Googliness/GCA)." if company else ""}
        
        CONTEXT:
        {f"Job Description: {jd}" if jd else ""}
        {f"Candidate Resume: {resume_text}" if resume_text else ""}
        
        YOUR GOAL:
        - Ask ONE question at a time.
        - BE CREATIVE: Do not ask common, overused questions. Create realistic but fresh scenarios that test deep understanding.
        - Focus heavily on {round_name} topics.
        - If a resume is provided, tie questions to their actual projects when relevant.
        - Maintain the persona of a {company if company else "standard"} interviewer: be professional, probing, and strict.
        - NO SUGARCOATING: If the candidate is struggling, probe deeper into their weakness.
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
        """Evaluates a single answer with total honesty and zero sugarcoating."""
        prompt = f"""
        Interviewer Persona: Senior Lead at {company if company else "a Top Tech Firm"}
        Role: {role}
        Question: {question}
        User Answer: {answer}
        
        TASK:
        Evaluate this answer with extreme honesty. If it's a "standard" or "memorized" answer, penalize it. 
        We want to see deep thinking, not just definitions.
        
        RATING CRITERIA (1-10):
        10: Mind-blowing, unique, and technically perfect.
        7-8: Solid, industry standard.
        5-6: Needs significant work, too generic.
        <4: Reject.
        
        FEEDBACK STYLE:
        - NO SUGARCOATING. Be direct. If the answer was bad, say why clearly.
        - Do not say "Good job" unless it was truly exceptional.
        
        Return the result in JSON format:
        {{
            "score": float,
            "feedback": "string (honest & direct)",
            "strengths": [],
            "weaknesses": [],
            "can_proceed": boolean (True only if score >= 7)
        }}
        """
        
        response = self.model.generate_content(prompt)
        return response.text

gemini_service = GeminiService()
