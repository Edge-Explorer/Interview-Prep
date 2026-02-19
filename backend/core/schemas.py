from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class InterviewCreate(BaseModel):
    role_category: str
    sub_role: str
    difficulty_level: int = 1
    job_description: Optional[str] = None
    target_company: Optional[str] = None
    is_panel: bool = False
    interviewer_name: str = "Adinath"

class InterviewResponse(BaseModel):
    id: int
    role_category: str
    sub_role: str
    first_question: str
    created_at: datetime

    class Config:
        from_attributes = True

class AnswerSubmit(BaseModel):
    interview_id: int
    answer: str

class EvaluationResponse(BaseModel):
    score: float
    feedback: str
    vibe_analysis: Optional[dict] = None
    next_question: Optional[str] = None
    can_proceed: bool = True

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_premium: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
