from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, database
from services.gemini_service import gemini_service

app = FastAPI(
    title="Interview Prep AI Platform",
    description="AI-powered interview preparation platform using Gemini 2.0 Flash",
    version="1.0.1",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to InterviewAI Backend", "status": "online"}

@app.post("/interviews/start", response_model=schemas.InterviewResponse)
async def start_interview(data: schemas.InterviewCreate, db: Session = Depends(database.get_db)):
    # 1. Generate the very first question using Gemini
    first_question = await gemini_service.generate_interview_question(
        role=data.role_category,
        sub_role=data.sub_role,
        difficulty=data.difficulty_level,
        jd=data.job_description
    )

    # 2. Save session to DB (User ID hardcoded to 1 for now until Auth is added)
    new_session = models.InterviewSession(
        user_id=1, 
        role_category=data.role_category,
        sub_role=data.sub_role,
        difficulty_level=data.difficulty_level,
        job_description=data.job_description,
        transcript=[{"role": "assistant", "content": first_question}]
    )
    
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return {
        "id": new_session.id,
        "role_category": new_session.role_category,
        "sub_role": new_session.sub_role,
        "first_question": first_question,
        "created_at": new_session.created_at
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
