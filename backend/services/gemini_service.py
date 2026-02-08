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

    async def generate_interview_question(self, role: str, sub_role: str, difficulty: int, jd: str = None, resume_text: str = None, chat_history: list = []):
        """Generates a contextual interview question based on role, difficulty, resume, and history."""
        
        difficulty_map = {1: "Junior", 2: "Mid-level", 3: "Senior/Lead"}
        level = difficulty_map.get(difficulty, "Junior")

        system_prompt = f"""
        You are an expert professional interviewer for the position of {sub_role} ({role} category).
        The candidate is applying for a {level} role.
        
        CONTEXT:
        {f"Job Description: {jd}" if jd else "General industry standard for this role."}
        {f"Candidate Resume: {resume_text}" if resume_text else ""}
        
        YOUR GOAL:
        - Ask ONE question at a time.
        - If a resume is provided, start by cross-referencing their experience with the job requirements.
        - Ask about specific projects or skills mentioned in their resume to verify authenticity.
        - If there is chat history, listen to the candidate's last answer and ask a relevant follow-up.
        - For {level} roles, ensure the depth of the question matches the expectations.
        - If the user asks about a role you don't recognize, use your internal knowledge to adapt based on their resume/JD.
        """

        # Prepare chat history for Gemini
        # (Converting our DB JSON format to Gemini format)
        contents = [{"role": "user" if i % 2 == 0 else "model", "parts": [m]} for i, m in enumerate(chat_history)]
        
        # Add the system prompt/instruction
        # Starting the chat
        chat = self.model.start_chat(history=contents)
        response = chat.send_message(f"Assistant: Please ask the first or next question for the {sub_role} interview.")
        
        return response.text

    async def evaluate_answer(self, question: str, answer: str, role: str):
        """Evaluates a single answer and provides feedback + score."""
        prompt = f"""
        Role: {role}
        Question: {question}
        User Answer: {answer}
        
        Evaluate this answer on a scale of 1-10. 
        Provide:
        1. Score (JSON format: "score": 8)
        2. Strengths: What did they do well?
        3. Weaknesses: What was missing?
        4. Modern Tip: One pro-tip to make this answer stand out (mentoring).
        """
        
        response = self.model.generate_content(prompt)
        return response.text

gemini_service = GeminiService()
