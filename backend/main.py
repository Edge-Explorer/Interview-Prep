from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, database
from services.gemini_service import gemini_service
import pypdf
import io
import json
from datetime import datetime
import auth_utils
from services.intelligence_service import get_intelligence_service

app = FastAPI(
    title="Interview Prep AI Platform",
    description="AI-powered interview preparation platform using Gemini 2.0 Flash",
    version="2.1.0",
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
    return {"status": "ok", "version": "2.1.0"}

# --- AUTH ENDPOINTS ---
@app.post("/auth/signup", response_model=schemas.Token)
async def signup(user_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Check if user exists
    db_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_pass = auth_utils.get_password_hash(user_data.password)
    new_user = models.User(
        email=user_data.email,
        hashed_password=hashed_pass,
        full_name=user_data.full_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate token
    access_token = auth_utils.create_access_token(data={"sub": new_user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": new_user
    }

@app.post("/auth/login", response_model=schemas.Token)
async def login(login_data: schemas.UserLogin, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == login_data.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not auth_utils.verify_password(login_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = auth_utils.create_access_token(data={"sub": db_user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": db_user
    }

@app.get("/users/stats")
async def get_user_stats(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth_utils.get_current_user)):
    interviews = db.query(models.InterviewSession).filter(models.InterviewSession.user_id == current_user.id).all()
    
    total_interviews = len(interviews)
    
    # Calculate average score from all sessions
    scores = [i.score for i in interviews if i.score is not None]
    avg_score = sum(scores) / len(scores) if scores else 0.0
    
    return {
        "total_interviews": total_interviews,
        "avg_score": round(avg_score, 1)
    }

# --- INTERVIEW ENDPOINTS ---

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
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth_utils.get_current_user)
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
        user_id=current_user.id, 
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
async def submit_answer(
    data: schemas.AnswerSubmit, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth_utils.get_current_user)
):
    from round_config import ROUND_DEFINITIONS, get_next_round, should_proceed_to_next_round
    
    # 1. Fetch current session
    session = db.query(models.InterviewSession).filter(
        models.InterviewSession.id == data.interview_id,
        models.InterviewSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Interview not found or unauthorized")

    # 2. Update transcript with user's answer
    session.transcript.append({"role": "user", "content": data.answer})
    session.questions_count += 1
    
    # 3. Get current round configuration
    current_round_config = ROUND_DEFINITIONS.get(session.current_round_number, ROUND_DEFINITIONS[1])
    MIN_QUESTIONS = current_round_config["min_questions"]
    MAX_QUESTIONS = current_round_config["max_questions"]
    
    # 4. Determine if we should continue or evaluate current round
    if session.questions_count < MIN_QUESTIONS:
        # Continue asking questions in current round - NO EVALUATION YET
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
            "evaluation": None,
            "next_question": next_question,
            "terminated": False,
            "round_completed": False,
            "current_round": session.interview_round,
            "current_round_number": session.current_round_number,
            "questions_asked": session.questions_count
        }
    else:
        # Evaluate current round after sufficient questions
        last_question = next((m["content"] for m in reversed(session.transcript) if m["role"] == "assistant"), None)
        
        # Get tailored intelligence (DATABASE -> AGENT -> FALLBACK)
        try:
            intel_service = get_intelligence_service()
            # Pass job_description to help agents reverse-engineer stealth companies
            company_intel = await intel_service.get_intelligence(
                session.target_company, 
                session.job_description
            )
        except Exception as e:
            print(f"Error fetching company intelligence: {e}")
            company_intel = None

        # Evaluate using Gemini with round-specific criteria
        evaluation_raw = await gemini_service.evaluate_answer(
            question=last_question,
            answer=data.answer,
            role=session.role_category,
            round_name=session.interview_round,
            company=session.target_company,
            company_intel=company_intel # Pass company intelligence to evaluation
        )

        # Clean the JSON from Gemini
        clean_json = evaluation_raw.replace('```json', '').replace('```', '').strip()
        try:
            eval_data = json.loads(clean_json)
        except:
            eval_data = {"score": 5, "feedback": evaluation_raw, "can_proceed": False}

        current_score = eval_data.get("score", 0)
        session.score = current_score
        
        # Store round score
        if not session.round_scores:
            session.round_scores = {}
        session.round_scores[session.interview_round] = current_score
        
        # Check if candidate passed this round
        passed_round = should_proceed_to_next_round(current_score, session.current_round_number)
        
        if passed_round:
            # Check if there's a next round
            next_round_number = get_next_round(
                session.current_round_number,
                session.role_category,
                session.difficulty_level
            )
            
            if next_round_number:
                # Progress to next round
                session.rounds_completed.append(session.interview_round)
                session.current_round_number = next_round_number
                session.interview_round = ROUND_DEFINITIONS[next_round_number]["name"]
                session.questions_count = 0  # Reset for new round
                session.transcript = []  # Clear transcript for new round
                
                # Generate first question of next round
                current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                next_question = await gemini_service.generate_interview_question(
                    role=session.role_category,
                    sub_role=session.sub_role,
                    difficulty=session.difficulty_level,
                    company=session.target_company,
                    round_name=session.interview_round,
                    jd=session.job_description,
                    resume_text=session.resume_text,
                    chat_history=[],
                    current_time=current_time_str,
                    interviewer_name=session.interviewer_name
                )
                session.transcript.append({"role": "assistant", "content": next_question})
                db.commit()
                
                return {
                    "evaluation": eval_data,
                    "next_question": next_question,
                    "terminated": False,
                    "round_completed": True,
                    "round_passed": True,
                    "next_round": session.interview_round,
                    "next_round_number": session.current_round_number,
                    "rounds_completed": session.rounds_completed,
                    "round_scores": session.round_scores,
                    "questions_asked": session.questions_count
                }
            else:
                # No more rounds - Interview complete!
                session.rounds_completed.append(session.interview_round)
                session.overall_status = "completed"
                db.commit()
                
                return {
                    "evaluation": eval_data,
                    "next_question": None,
                    "terminated": True,
                    "round_completed": True,
                    "round_passed": True,
                    "interview_completed": True,
                    "rounds_completed": session.rounds_completed,
                    "round_scores": session.round_scores,
                    "overall_message": "Congratulations! You've completed all interview rounds!"
                }
        else:
            # Failed current round - Terminate interview
            session.overall_status = "failed"
            db.commit()
            
            return {
                "evaluation": eval_data,
                "next_question": None,
                "terminated": True,
                "round_completed": True,
                "round_passed": False,
                "failed_round": session.interview_round,
                "rounds_completed": session.rounds_completed,
                "round_scores": session.round_scores,
                "overall_message": f"Interview terminated. You did not pass the {session.interview_round} round."
            }
@app.post("/interviews/start", response_model=schemas.InterviewResponse)
async def start_interview(
    data: schemas.InterviewCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth_utils.get_current_user)
):
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

    # 2. Save session to DB
    new_session = models.InterviewSession(
        user_id=current_user.id, 
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
