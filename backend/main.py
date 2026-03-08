from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from core import models, schemas, database
from services.gemini_service import gemini_service
import pypdf
import io
import json
import asyncio
from datetime import datetime
from auth import auth_utils
from services.intelligence_service import get_intelligence_service
from services.memory_service import get_memory_service
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events."""
    print("LOG: Application is booting up...")
    # Temporarily back to Lazy Loading to resolve the 4GB VRAM overflow error
    get_intelligence_service(eager_load=False)
    yield
    print("LOG: Application is shutting down...")

app = FastAPI(
    title="Interview Prep AI Platform",
    description="AI-powered interview preparation platform using Gemini 2.0 Flash",
    version="2.1.0",
    lifespan=lifespan
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
    # Legacy authentication disabled in favor of Google OAuth
    raise HTTPException(status_code=403, detail="Standard signup is disabled. Please use Google Sign-in.")

@app.post("/auth/login", response_model=schemas.Token)
async def login(login_data: schemas.UserLogin, db: Session = Depends(database.get_db)):
    # Legacy authentication disabled in favor of Google OAuth
    raise HTTPException(status_code=403, detail="Standard login is disabled. Please use Google Sign-in.")

@app.post("/auth/google", response_model=schemas.Token)
async def google_login(data: schemas.GoogleLoginRequest, db: Session = Depends(database.get_db)):
    try:
        # 1. Verify Google Token
        CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
        idinfo = id_token.verify_oauth2_token(data.token, google_requests.Request(), CLIENT_ID)

        # 2. Get user info from Google
        email = idinfo['email']
        full_name = idinfo.get('name', '')
        
        # 3. Check if user exists
        db_user = db.query(models.User).filter(models.User.email == email).first()
        
        if not db_user:
            # Create a new user (Auto-registration)
            db_user = models.User(
                email=email,
                full_name=full_name,
                hashed_password="GOOGLE_AUTH_USER", # No password needed for OAuth
                is_premium=0
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            
        # 4. Generate our app's JWT
        access_token = auth_utils.create_access_token(data={"sub": db_user.email})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": db_user
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Google token")
    except Exception as e:
        print(f"Error in Google login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during Google login")

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

@app.get("/interviews/companies/suggestions")
async def get_company_suggestions(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth_utils.get_current_user)):
    """Returns an exhaustive list of all known companies from ALL sources for frontend autocomplete."""
    suggestions = set()
    
    # 1. Curated Profiles (Main Database)
    try:
        curated_inst = get_company_intelligence()
        suggestions.update(curated_inst.get_all_companies())
    except Exception as e:
        print(f"DEBUG: Failed to load curated companies: {e}")
    
    # 2. Project Data Files
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "data")
        
        # Gold Discoveries (AI Scanned)
        gold_path = os.path.join(data_dir, "discoveries.json")
        if os.path.exists(gold_path):
            with open(gold_path, 'r', encoding='utf-8') as f:
                gold_data = json.load(f)
                if isinstance(gold_data, list):
                    for d in gold_data:
                        name = d.get('company_name')
                        if name: suggestions.add(name)
        
        # Stealth Registry (Internal Tracking)
        stealth_path = os.path.join(data_dir, "stealth_registry.json")
        if os.path.exists(stealth_path):
            with open(stealth_path, 'r', encoding='utf-8') as f:
                stealth_data = json.load(f)
                if isinstance(stealth_data, dict):
                    suggestions.update(stealth_data.keys())
                    
    except Exception as e:
        print(f"DEBUG: Failed to load data markers: {e}")
    
    # Clean and sort: remove empty strings, Nones, and specific placeholders
    final_list = sorted([s for s in suggestions if s and s.lower() not in ["none", "null", "undefined"]])
    return final_list
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
    from core.round_config import get_first_round

    # 1. Extract text from PDF
    try:
        pdf_reader = pypdf.PdfReader(io.BytesIO(await file.read()))
        resume_text = ""
        for page in pdf_reader.pages:
            resume_text += page.extract_text()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Could not read PDF file")

    # 1. Start Foundation tasks (Intel and Analysis)
    intel_service = get_intelligence_service()
    intel_task = asyncio.create_task(intel_service.get_intelligence(target_company, job_description)) if target_company else None
    analysis_task = asyncio.create_task(gemini_service.analyze_resume(resume_text, job_description))

    print(f"LOG: Parallel extraction started for {target_company or 'General Resume'}...")
    
    # Wait for the foundation data (up to 60s for deep discovery)
    foundation_tasks = [analysis_task]
    if intel_task:
        foundation_tasks.append(intel_task)
    
    await asyncio.wait(foundation_tasks, timeout=60.0)
    
    # Extract results
    analysis_raw = analysis_task.result() if analysis_task.done() and not analysis_task.exception() else "Analysis timed out."
    company_intel = intel_task.result() if intel_task and intel_task.done() and not intel_task.exception() else None
    
    # 2. Now generate the FIRST QUESTION using the intel we just got
    print("LOG: Generating first contextual question...")
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
        interviewer_name=interviewer_name,
        company_intel=company_intel
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
        interview_round=get_first_round(role_category, difficulty_level),
        transcript=[{"role": "assistant", "content": first_question}]
    )
    
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return {
        "id": new_session.id,
        "first_question": first_question,
        "resume_analysis": analysis_raw,
        "company_intelligence": company_intel
    }

@app.post("/interviews/submit-answer")
async def submit_answer(
    data: schemas.AnswerSubmit, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth_utils.get_current_user)
):
    from core.round_config import get_round_config, get_next_round, should_proceed_to_next_round
    
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
    
    # 3. Get current round configuration by NAME (domain-aware)
    current_round_config = get_round_config(session.interview_round)
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
        passed_round = should_proceed_to_next_round(current_score, session.interview_round)
        
        if passed_round:
            # Check if there's a next round
            # Get next round NAME for this domain
            next_round_name = get_next_round(
                session.interview_round,
                session.role_category,
                session.difficulty_level
            )
            
            if next_round_name:
                # Progress to next round
                session.rounds_completed.append(session.interview_round)
                session.current_round_number += 1  # increment index for tracking
                session.interview_round = next_round_name
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
                if session.interview_round not in session.rounds_completed:
                    session.rounds_completed.append(session.interview_round)
                session.overall_status = "completed"
                
                # Generate Master Report (Executive Scorecard)
                session_dict = {
                    "transcript": session.transcript,
                    "round_scores": session.round_scores,
                    "sub_role": session.sub_role,
                    "target_company": session.target_company
                }
                master_report_raw = await gemini_service.generate_master_report(session_dict)
                clean_report_json = master_report_raw.replace('```json', '').replace('```', '').strip()
                try:
                    master_report = json.loads(clean_report_json)
                except:
                    master_report = {
                        "overall_score": sum(session.round_scores.values()) / len(session.round_scores) if session.round_scores else session.score,
                        "final_verdict": "HIRE",
                        "recruiter_closing_note": master_report_raw
                    }

                db.commit()

                # TIERED LEARNING: Save to Crowdsourced Stealth Registry
                try:
                    memory_service = get_memory_service()
                    session_full_data = {
                        "target_company": session.target_company,
                        "role_category": session.role_category,
                        "rounds_completed": session.rounds_completed,
                        "score": sum(session.round_scores.values()) / len(session.round_scores) if session.round_scores else session.score
                    }
                    await memory_service.learn_from_session(session_full_data, eval_data)
                except Exception as e:
                    print(f"ERROR: Memory Learning failed: {e}")
                
                return {
                    "evaluation": eval_data,
                    "master_report": master_report,
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
            session.overall_status = "failed"
            db.commit()

            # TIERED LEARNING: Save struggle/failure data (Structural only)
            try:
                memory_service = get_memory_service()
                session_full_data = {
                    "target_company": session.target_company,
                    "role_category": session.role_category,
                    "rounds_completed": session.rounds_completed + [session.interview_round],
                    "score": session.score
                }
                await memory_service.learn_from_session(session_full_data, eval_data)
            except Exception as e:
                print(f"ERROR: Struggle Memory Learning failed: {e}")
            
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
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 1. Fetch Company Intelligence FIRST (Task)
    print(f"LOG: Initializing non-resume interview for {data.target_company}...")
    intel_task = None
    if data.target_company:
        intel_service = get_intelligence_service()
        intel_task = asyncio.create_task(intel_service.get_intelligence(data.target_company, data.job_description))

    # Wait for intel (Discovery is the bottleneck)
    company_intel = None
    if intel_task:
        await asyncio.wait([intel_task], timeout=60.0)
        company_intel = intel_task.result() if intel_task.done() and not intel_task.exception() else None
        if intel_task and not intel_task.done():
            print("WARNING: Start-Discovery timeout. Proceeding with industry defaults.")

    # 2. Now generate the FIRST QUESTION with context
    print("LOG: Generating first contextual question...")
    first_question = await gemini_service.generate_interview_question(
        role=data.role_category,
        sub_role=data.sub_role,
        difficulty=data.difficulty_level,
        company=data.target_company,
        is_panel=data.is_panel,
        jd=data.job_description,
        current_time=current_time_str,
        interviewer_name=data.interviewer_name,
        company_intel=company_intel
    )

    from core.round_config import get_first_round

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
        interview_round=get_first_round(data.role_category, data.difficulty_level),
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
        "company_intelligence": company_intel,
        "created_at": new_session.created_at
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
