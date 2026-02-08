from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_premium = Column(Integer, default=0) # 0: Free, 1: Premium
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class InterviewSession(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_category = Column(String) # e.g., "SDE", "Data Science", "HR"
    sub_role = Column(String) # e.g., "ML Engineer", "SDE2"
    difficulty_level = Column(Integer, default=1) # 1: Junior, 2: Mid, 3: Senior
    job_description = Column(Text, nullable=True)
    resume_text = Column(Text, nullable=True) # Extracted text from uploaded resume
    ats_score = Column(Float, nullable=True) # Premium feature
    resume_analysis = Column(JSON, nullable=True) # Detailed strengths/weaknesses
    transcript = Column(JSON, default=[]) # Stores the chat history
    score = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    upi_transaction_id = Column(String, unique=True)
    status = Column(String) # SUCCESS, PENDING, FAILED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
