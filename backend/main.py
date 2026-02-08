from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, database
from services.gemini_service import gemini_service
import pypdf
import io
import json

app = FastAPI(
    title="Interview Prep AI Platform",
    description="AI-powered interview preparation platform using Gemini 2.0 Flash",
    version="1.0.1",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.1"}

@app.post("/interviews/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    role_category: str = Form(...),
    sub_role: str = Form(...),
    difficulty_level: int = Form(1),
    target_company: str = Form(None),
    is_panel: bool = Form(False),
    job_description: str = Form(None),
    db: Session = Depends(database.get_db)
):
    # 1. Extract text from PDF
    try:
        pdf_reader = pypdf.PdfReader(io.BytesIO(await file.read()))
        resume_text = ""
        for page in pdf_reader.pages:
            resume_text += page.extract_text()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Could not read PDF file")

    # 2. Premium Feature: Comprehensive Resume Analysis
    analysis_raw = await gemini_service.analyze_resume(resume_text, job_description)
    
    # 3. Generate first question using Resume Context
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    first_question = await gemini_service.generate_interview_question(
        role=role_category,
        sub_role=sub_role,
        difficulty=difficulty_level,
        company=target_company,
        is_panel=is_panel,
        jd=job_description,
        resume_text=resume_text,
        current_time=current_time_str
    )

    # 4. Save to DB
    clean_analysis = analysis_raw.replace('```json', '').replace('```', '').strip()
    try:
        analysis_obj = json.loads(clean_analysis)
    except:
        analysis_obj = analysis_raw

    new_session = models.InterviewSession(
        user_id=None, # Guest session
        role_category=role_category,
        sub_role=sub_role,
        difficulty_level=difficulty_level,
        target_company=target_company,
        is_panel=int(is_panel),
        job_description=job_description,
        resume_text=resume_text,
        resume_analysis=analysis_obj,
        transcript=[{"role": "assistant", "content": first_question}]
    )
    
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return {
        "id": new_session.id,
        "first_question": first_question,
        "resume_analysis": analysis_raw
    }

@app.post("/interviews/submit-answer")
async def submit_answer(data: schemas.AnswerSubmit, db: Session = Depends(database.get_db)):
    # 1. Fetch current session
    session = db.query(models.InterviewSession).filter(models.InterviewSession.id == data.interview_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Interview not found")

    # 2. Extract last question from transcript
    last_question = next((m["content"] for m in reversed(session.transcript) if m["role"] == "assistant"), None)

    # 3. Evaluate using Gemini
    evaluation_raw = await gemini_service.evaluate_answer(
        question=last_question,
        answer=data.answer,
        role=session.role_category,
        company=session.target_company
    )

    # Clean the JSON from Gemini (remove markdown backticks if present)
    clean_json = evaluation_raw.replace('```json', '').replace('```', '').strip()
    try:
        eval_data = json.loads(clean_json)
    except:
        # Fallback if AI fails to return clean JSON
        eval_data = {"score": 5, "feedback": evaluation_raw, "can_proceed": False}

    # 4. Update Stats
    session.transcript.append({"role": "user", "content": data.answer})
    session.questions_count += 1
    current_score = eval_data.get("score", 0)
    session.score = current_score # Latest performance
    
    # 5. Handle Gating (Realistic Round Logic)
    # Don't terminate immediately unless it's a catastrophic failure (score < 3)
    # Otherwise, ask at least 3 questions before deciding.
    MIN_QUESTIONS_PER_ROUND = 3
    is_catastrophic = current_score < 3
    should_continue = not is_catastrophic and session.questions_count < MIN_QUESTIONS_PER_ROUND
    
    # If we haven't reached min questions OR they are doing well, continue
    if should_continue or (current_score >= 7 and session.questions_count < 10): # Limit to max 10
        current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        next_question = await gemini_service.generate_interview_question(
            role=session.role_category,
            sub_role=session.sub_role,
            difficulty=session.difficulty_level,
            company=session.target_company,
            round_name=session.interview_round,
            jd=session.job_description,
            resume_text=session.resume_text,
            chat_history=[m["content"] for m in session.transcript],
            current_time=current_time_str
        )
        session.transcript.append({"role": "assistant", "content": next_question})
        terminated = False
    else:
        # Final decision point
        next_question = None
        terminated = True
    
    db.commit()

    return {
        "evaluation": eval_data,
        "next_question": next_question,
        "terminated": terminated,
        "questions_asked": session.questions_count
    }
@app.post("/interviews/start", response_model=schemas.InterviewResponse)
async def start_interview(data: schemas.InterviewCreate, db: Session = Depends(database.get_db)):
    # 1. Generate the very first question using Gemini
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    first_question = await gemini_service.generate_interview_question(
        role=data.role_category,
        sub_role=data.sub_role,
        difficulty=data.difficulty_level,
        company=data.target_company,
        is_panel=data.is_panel,
        jd=data.job_description,
        current_time=current_time_str
    )

    # 2. Save session to DB (Guest session for now)
    new_session = models.InterviewSession(
        user_id=None, 
        role_category=data.role_category,
        sub_role=data.sub_role,
        difficulty_level=data.difficulty_level,
        target_company=data.target_company,
        is_panel=int(data.is_panel),
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
