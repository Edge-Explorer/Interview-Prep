from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, database
from services.gemini_service import gemini_service
import pypdf
import io
import json
from datetime import datetime

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
    interviewer_name: str = Form("Adinath"),
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
        current_time=current_time_str,
        interviewer_name=interviewer_name
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
        interviewer_name=interviewer_name,
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

    # 2. Update transcript with user's answer
    session.transcript.append({"role": "user", "content": data.answer})
    session.questions_count += 1
    
    # 3. Define interview parameters
    MIN_QUESTIONS = 5  # Minimum questions before evaluation
    MAX_QUESTIONS = 10  # Maximum questions in one round
    
    # 4. Determine if we should continue or evaluate
    should_continue = session.questions_count < MIN_QUESTIONS
    
    if should_continue or session.questions_count < MAX_QUESTIONS:
        # Continue asking questions - NO EVALUATION YET
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
            current_time=current_time_str,
            interviewer_name=session.interviewer_name
        )
        session.transcript.append({"role": "assistant", "content": next_question})
        db.commit()
        
        return {
            "evaluation": None,  # No evaluation until minimum questions reached
            "next_question": next_question,
            "terminated": False,
            "questions_asked": session.questions_count
        }
    else:
        # NOW evaluate after asking sufficient questions
        # Extract last question from transcript
        last_question = next((m["content"] for m in reversed(session.transcript) if m["role"] == "assistant"), None)
        
        # Evaluate using Gemini
        evaluation_raw = await gemini_service.evaluate_answer(
            question=last_question,
            answer=data.answer,
            role=session.role_category,
            company=session.target_company
        )

        # Clean the JSON from Gemini
        clean_json = evaluation_raw.replace('```json', '').replace('```', '').strip()
        try:
            eval_data = json.loads(clean_json)
        except:
            eval_data = {"score": 5, "feedback": evaluation_raw, "can_proceed": False}

        session.score = eval_data.get("score", 0)
        db.commit()

        return {
            "evaluation": eval_data,
            "next_question": None,
            "terminated": True,
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
        current_time=current_time_str,
        interviewer_name=data.interviewer_name
    )

    # 2. Save session to DB (Guest session for now)
    new_session = models.InterviewSession(
        user_id=None, 
        role_category=data.role_category,
        sub_role=data.sub_role,
        difficulty_level=data.difficulty_level,
        target_company=data.target_company,
        is_panel=int(data.is_panel),
        interviewer_name=data.interviewer_name,
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
