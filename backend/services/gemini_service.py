import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    async def generate_interview_question(self, role: str, sub_role: str, difficulty: int, jd: str = None, chat_history: list = []):
        """Generates a contextual interview question based on role, difficulty, and history."""
        
        difficulty_map = {1: "Junior", 2: "Mid-level", 3: "Senior/Lead"}
        level = difficulty_map.get(difficulty, "Junior")

        system_prompt = f"""
        You are an expert professional interviewer for the position of {sub_role} ({role} category).
        The candidate is applying for a {level} role.
        
        CONTEXT:
        {f"Job Description: {jd}" if jd else "General industry standard for this role."}
        
        YOUR GOAL:
        - Ask ONE technical or behavioral question at a time.
        - If there is chat history, listen to the candidate's last answer and ask a relevant follow-up or a new topic question.
        - Do not give answers. Be professional, slightly tough but fair.
        - For {level} roles, ensure the depth of the question matches the expectations.
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
