# 🎯 InterviewAI - Professional Interview Intelligence Platform

**Created & Authored by: [Karan Shelar](https://github.com/Edge-Explorer)**

---

> 📚 **Project Docs:** &nbsp;[Challenges](./docs/CHALLENGES.md) &nbsp;|&nbsp; [Next Steps](./docs/NEXT_STEPS.md) &nbsp;|&nbsp; [Coding Round Design](./docs/CODING_ROUND_DESIGN.md) &nbsp;|&nbsp; [Technical Flow](./docs/TECHNICAL_FLOW.md) &nbsp;|&nbsp; [Collaborators](./docs/COLLABORATORS.md) &nbsp;|&nbsp; [All Docs →](./docs/)

---
<div align="center">

![Version](https://img.shields.io/badge/version-2.4.0-blue.svg)
![Status](https://img.shields.io/badge/status-Executive%20Memory-purple.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![React](https://img.shields.io/badge/react-18.3+-61DAFB.svg)
![Gemini](https://img.shields.io/badge/Gemini-2.0%20Flash-orange.svg)
![Llama3](https://img.shields.io/badge/Agentic-Llama--3--8B-red.svg)

## 🌟 The Simulation Philosophy

InterviewAI is not just a "mock interview" tool; it is an **Advanced Intelligent Simulation Entity**. While traditional platforms rely on static question banks, InterviewAI uses a **Dynamic Agentic Loop** to synthesize the reality of the 2025/2026 job market.

### 🎭 The Persona Architecture
We don't just ask questions; we simulate **Human Personalities**:
*   **Adinath (The Primal Sage)**: Simulates the "Foundation First" interviewer. He is cold, direct, and explores the recursive depth of your technical architecture. He tests the "How" and the "Why."
*   **Veda (The Eternal Wisdom)**: Simulates the "Clarity Specialist." She is observant, testing your vision, cultural alignment, and your ability to communicate complex ideas under pressure.

---

## 🚀 Technical Innovation: The "Agentic Edge" (v2.3 — Domain-Aware Round Engine)

What makes this project unique in the industry is its **Three-Tier Intelligence Architecture**, designed to solve the "Knowledge Gap" in AI:

1.  **The Curated Core**: Local access to **402 expert-verified company profiles** across 12 domains for zero-latency, reliable data.
2.  **The Agentic Discovery Loop (LangGraph)**: An autonomous multi-agent team that researches public companies in real-time.
    *   **Dynamic Domain Intelligence**: Automatically prevents "Role Forcing" (e.g., won't force LeetCode questions on a legal or clinical role).
    *   **Geographic Guardrails**: Prevents acronym collisions (e.g., identifying **MOC Cancer Care India** vs **Moffitt USA**) by localized search auditing.
    *   **Generic Article Purge**: Python-level domain blocklist strips SEO junk (datacamp, guru99, intellipaat, etc.) before the AI ever sees the data.
3.  **Stealth Mode & Synthetic Fallback**: A world-first feature that **Reverse-Engineers company DNA** from a Job Description. If a company is in "Stealth Mode" (non-public), the AI synthesizes a high-fidelity interview based on industry-standard benchmarking.
4.  **Domain-Aware Round Engine (v2.3)**: Each of the 12 career domains gets its own interview structure — Finance gets Case Study rounds, Healthcare gets Situational/Clinical rounds, Creative gets Portfolio Review. No more forcing tech candidates' rounds onto Accounting or Legal applicants.
5.  **Crowdsourced Self-Learning Memory (v2.4)**: The system now learns from its users. The **Stealth Registry** implements a "Witness vs Expert" consensus logic. It builds high-fidelity profiles for private startups by aggregating data from persistent "Strugglers" (Structural Roadmap) and Top-Performers (Success Criteria).

### 🛡️ Confidence Score Guide
The system now provides transparency on how it "trusts" the discovered intelligence:

| Score | Status | Description | Reliability |
| :--- | :--- | :--- | :--- |
| **0 - 20** | **Synthetic** | No public info found. AI "guesstimates" based strictly on the Industry & JD. | ⚠️ Experimental |
| **85** | **Verified** | Sufficient public sources found. Identity is verified. | ✅ High |
| **100 - 160** | **Elite Certified** | Extreme certainty. Matched Location, Industry, and found Direct Interview Questions. | 🏆 Production Grade |

---

## 🏗️ System Architecture

```mermaid
graph TD
    User((User)) -->|"Uploads Resume/JD"| UI["React Dashboard"]
    UI -->|Trigger| Backend["FastAPI Core"]
    
    subgraph "The Intelligence Brain"
        Backend --> Gatekeeper{Entry Gate}
        Gatekeeper -->|Found| DB["Curated 402 DB"]
        Gatekeeper -->|"Not Found"| Agents["LangGraph Research Team"]
        
        Agents --> Router["Router (Location Guard)"]
        Router --> Researcher["DuckDuckGo Researcher"]
        Researcher --> Auditor["Auditor Agent - The Bouncer"]
        Auditor --> Architect["Architect (Llama-3 Profile Builder)"]
        Architect --> Critic["Gemini Quality Validator"]
        
        Critic -->|Approved| Memory[("(discoveries.json)")]
        Memory --> Context["Simulation Context"]
        DB --> Context
    end
    
    Context -->|Seed| Simulation["Gemini 2.0 Simulation"]
    Simulation -->|"Voice/Video"| User
    Simulation -->|Feedback| Persistence[("Neon Cloud PostgreSQL")]
```

---

## ✅ Development Progress

###  **Phase 1: Core Foundation** (COMPLETED ✅)

#### Backend Infrastructure
- [x] FastAPI application setup with CORS
- [x] PostgreSQL database integration (Neon Cloud)
- [x] SQLAlchemy ORM models
- [x] Alembic migration system (Production Sync Ready)
- [x] Gemini 2.0 Flash API integration
- [x] PDF resume parsing (PyPDF)
- [x] Session management system
- [x] RESTful API endpoints

#### Frontend Foundation
- [x] React + Vite setup
- [x] Component architecture
- [x] State management with hooks
- [x] Axios API integration
- [x] Web Speech API integration
- [x] Camera/microphone controls

#### AI Interview System
- [x] Multi-persona AI interviewers (Adinath & Veda)
- [x] Context-aware question generation
- [x] **Company Intelligence System (Advanced)**
  - [x] Tier 1: Curated database for **383 unique companies**
  - [x] Tier 2: **Agentic Discovery Memory** (`discoveries.json`)
  - [x] Tier 3: **Crowdsourced Stealth Registry** (`stealth_registry.json`) - *Self-Learning Layer*
  - [x] FAANG, AI Specialists, Indian Tech, Finance, Consulting, and Global Domains
  - [x] Company-specific interview styles and cultural values
  - [x] Round-specific focus areas and common topics
  - [x] Tier 4: AI fallback for unknown companies
- [x] **Fine-Tuned Intelligence (Llama-3-8B)**
  - [x] Custom LoRA adapters trained on 383-company dataset
  - [x] Hybrid Duo Logic: Llama-3 (Architect) + Gemini 2.0 (Communicator)
- [x] **Agentic Discovery System (LangGraph v2.2)**
  - [x] Multi-agent Router-Researcher-Auditor-Architect-Critic workflow
  - [x] **Dynamic Domain Logic**: Prevents 'Role Forcing' on non-tech industries.
  - [x] **Geographic Guarding**: Dedicated router to prevent name collisions across countries.
  - [x] **The Auditor (The Bouncer)**: Filters out noise/irrelevant data and verifies identity against JD
  - [x] **Evergreen Perpetual Freshness**: Dynamic temporal anchoring for search queries.
  - [x] **Stealth Mode Support**: Reverse-engineers JDs for private companies.
  - [x] **Discovery Memory**: Persistent learning layer with Consensus Vetting.
- [x] Company-specific simulations
- [x] Difficulty levels (Junior, Mid, Senior)
- [x] Panel interview mode
- [x] Resume-based personalization
- [x] Multi-Round Marathon (Technical -> Behavioral -> Managerial -> Final)
- [x] **Executive Scorecard & Analytics** (Option C)
  - [x] STAR Method Analysis (Situation, Task, Action, Result)
  - [x] Vibe Assessment (Confidence, Technical Depth, Assertiveness)
  - [x] Cumulative Performance Reports

#### Premium UI/UX
- [x] Industry-level glassmorphism design
- [x] Animated mesh gradients
- [x] Floating particle effects
- [x] 3D card transforms
- [x] Professional meeting interface
- [x] Compact toolbar design
- [x] Premium button hierarchy
- [x] Shimmer effects and micro-interactions
- [x] Responsive design
- [x] Camera blur fix and state management

---

## 🚧 Roadmap - What's Next

### 🔥 **Phase 2: Multi-Round Interview System** (PENDING 🔴)

#### Round 1: Technical/Screening Round
- [x] Basic implementation (CURRENT)
- [ ] Round-specific evaluation criteria
- [ ] Technical depth assessment
- [ ] Coding problem integration (optional)

#### Round 2: Behavioral/HR Round
- [ ] Behavioral question bank
- [ ] STAR method evaluation
- [ ] Cultural fit assessment
- [ ] Salary negotiation simulation
- [ ] Work-life balance discussions

#### Round 3: System Design Round (Technical Roles)
- [ ] System design problem generation
- [ ] Scalability discussion prompts
- [ ] Trade-off analysis evaluation
- [ ] Architecture diagram support (future)

#### Round 4: Managerial Round
- [ ] Leadership scenario questions
- [ ] Conflict resolution scenarios
- [ ] Team management assessment
- [ ] Strategic thinking evaluation

#### Round 5: Final/Director Round
- [ ] Vision and long-term goals
- [ ] Company culture alignment
- [ ] Executive presence evaluation
- [ ] Offer negotiation simulation

#### Non-Technical Interview Rounds
- [ ] **Healthcare & Medical**: Clinical scenarios, patient interaction
- [ ] **Business & Management**: Case studies, market analysis
- [ ] **Finance & Accounting**: Financial modeling, risk assessment
- [ ] **Creative & Design**: Portfolio review, design thinking
- [ ] **Sales & Marketing**: Pitch simulation, objection handling
- [ ] **Education & Training**: Teaching methodology, curriculum design
- [ ] **Legal**: Case analysis, ethical scenarios
- [ ] **Hospitality & Tourism**: Customer service scenarios

### � **Phase 3: Advanced Analytics & Scoring** (PENDING 🔴)

#### ATS & Resume Analysis
- [x] Basic resume parsing
- [x] Resume analysis endpoint
- [ ] **ATS Score Display** in UI
- [ ] **Gap Analysis Visualization**
- [ ] **Resume Improvement Suggestions** UI
- [ ] **Keyword Matching** against JD
- [ ] **Resume Rewriting Assistant**

#### Performance Analytics
- [ ] Multi-round score aggregation
- [ ] Performance trends over time
- [ ] Strengths/weaknesses dashboard
- [ ] Comparison with industry benchmarks
- [ ] Detailed transcript analysis
- [ ] Voice tone analysis (pitch, pace, clarity)
- [ ] Confidence score tracking

#### Behavioral Analysis
- [x] Basic vibe analysis in evaluation
- [ ] **Hesitation pattern detection**
- [ ] **Filler word counting** (um, uh, like)
- [ ] **Speaking pace analysis**
- [ ] **Assertiveness scoring**
- [ ] **Body language feedback** (if camera enabled)

### 🎓 **Phase 4: Learning & Growth** (PENDING 🔴)

#### Post-Interview Learning
- [ ] **7-Day Learning Roadmap** generation
- [ ] **Failed Topics Identification**
- [ ] **Resource Recommendations** (courses, articles, videos)
- [ ] **Practice Problem Sets**
- [ ] **Retry Interview** after learning period

#### Skill Development
- [ ] Personalized study plans
- [ ] Progress tracking
- [ ] Skill gap analysis
- [ ] Mock interview scheduling
- [ ] Peer comparison (anonymized)

### 🔐 **Phase 5: User Management & Authentication** (IN PROGRESS 🟡)

#### User System
- [x] Google OAuth Integration (Primary Login)
- [x] JWT-based Session Management (No random/false emails)
- [ ] User profiles
- [ ] Interview history
- [ ] Progress tracking
- [ ] Subscription management

#### Pricing Tiers & Payment
- [ ] **Free Tier**: 1 interview/2 weeks, basic feedback
- [ ] **Pro Tier** (₹199): Unlimited interviews, JD-tailored questions
- [ ] **Elite Tier** (₹499): Panel mode, 7-day roadmap, vibe analysis
- [ ] **UPI QR Code Payment** - Direct UPI payment (no gateway fees)
- [ ] Payment verification system
- [ ] Manual subscription activation after payment screenshot

#### UPI Payment Flow (Zero Cost)
1. User selects Pro/Elite tier
2. System displays **UPI QR Code** with amount
3. User pays via any UPI app (Google Pay, PhonePe, Paytm)
4. User uploads **payment screenshot**
5. Admin verifies payment (manual/automated OCR)
6. Subscription activated instantly
7. **No payment gateway fees** - 100% of payment received

### ☁️ **Phase 6: Deployment & Infrastructure** (PENDING 🔴)

#### Backend Deployment (AWS)
- [ ] **AWS EC2** - FastAPI backend hosting
- [ ] **AWS Elastic IP** - Static IP for backend
- [ ] **AWS Security Groups** - Firewall configuration
- [ ] **Nginx** - Reverse proxy setup
- [ ] **Gunicorn** - WSGI server for FastAPI
- [ ] Environment variable management
- [ ] SSL/TLS certificates (Let's Encrypt - Free)
- [ ] Auto-restart on failure (systemd)

#### Database Migration
- [ ] **Current**: PostgreSQL (pgAdmin4 - Local development)
- [ ] **Production**: Supabase PostgreSQL (Free tier - 500MB)
- [ ] Database migration from local to Supabase
- [ ] Connection pooling setup
- [ ] Backup strategy (Supabase auto-backup)
- [ ] Environment-based DB switching

#### Frontend Deployment
- [ ] **Vercel** deployment (Free tier)
- [ ] GitHub integration for auto-deploy
- [ ] Environment variable setup (API URL)
- [ ] Custom domain (free .vercel.app subdomain)
- [ ] CDN configuration (included)
- [ ] Performance optimization
- [ ] Analytics setup (Vercel Analytics - Free)

#### DevOps Pipeline
- [ ] **GitHub** - Source control & version management
- [ ] **GitHub Actions** - CI/CD pipeline (Free)
- [ ] Automated testing on PR
- [ ] Auto-deploy to Vercel on main branch push
- [ ] Backend deployment automation
- [ ] Database migration scripts
- [ ] Monitoring (AWS CloudWatch Free tier)
- [ ] Error tracking (Sentry Free tier)

### 🚀 **Phase 7: Advanced Features** (FUTURE 🔵)

#### AI Enhancements
- [ ] Voice cloning for more realistic interviewers
- [ ] Video avatar generation
- [ ] Real-time facial expression analysis
- [ ] Multi-language support
- [ ] Industry-specific jargon training

#### Collaboration Features
- [ ] Peer mock interviews
- [ ] Mentor review system
- [ ] Group interview simulations
- [ ] Interview recording playback
- [ ] Shareable interview reports

#### Integration & API
- [ ] LinkedIn integration
- [ ] Calendar integration (Google/Outlook)
- [ ] Slack notifications
- [ ] Email reports
- [ ] Public API for third-party integrations

---

## ✨ Current Features (v1.0.1)

### 🎤 **Live Interview Simulation**
- ✅ Real-time voice recognition for natural conversation
- ✅ Dynamic AI responses adapting to your answers
- ✅ Industry-standard UI with professional glassmorphism
- ✅ Live video feed with camera controls
- ✅ Minimum 5 questions before evaluation

### 🧠 **Intelligent Interview System**
- ✅ Multi-persona AI interviewers (Adinath & Veda)
- ✅ **Company Intelligence System (v2.0)**
  - ✅ Curated database for **383 companies** (20+ per major domain)
  - ✅ **Engineering & Tech**: Google, Amazon, Microsoft, Nvidia, Tesla, OpenAI (134 total)
  - ✅ **Healthcare & Medical**: Pfizer, Mayo Clinic, Johnson & Johnson, Pfizer (22 total)
  - ✅ **Finance & Accounting**: Goldman Sachs, JPMorgan, Stripe, Coinbase (22 total)
  - ✅ **Legal**: Kirkland & Ellis, DLA Piper, Latham & Watkins, Clio (22 total)
  - ✅ **Construction & Trades**: AECOM, Caterpillar, Larsen & Toubro, Vinci (23 total)
  - ✅ **Creative & Design**: Pixar, DreamWorks, Adobe, Vimeo, SoundCloud (21 total)
  - ✅ **Education & Training**: Coursera, Udacity, Khan Academy, Duolingo (21 total)
  - ✅ **Science & Research**: NASA, CERN, Max Planck, Bell Labs, ISRO (22 total)
  - ✅ **Social Services**: UNICEF, Bill & Melinda Gates Foundation, Red Cross (23 total)
  - ✅ **Hospitality & Tourism**: Airbnb, Marriott, Expedia, Hilton (21 total)
  - ✅ **Business & Management**: McKinsey, BCG, Deloitte, Accenture (23 total)
  - ✅ **Sales & Marketing**: Ogilvy, McCann, Leo Burnett, Dentsu (20 total)
  - ✅ **Agentic Intelligence**: Multi-agent orchestration for real-time web research with **Evergreen Perpetual Freshness**.
  - ✅ **Stealth Startup Support**: AI can "reverse-engineer" company DNA from any Job Description (JD)
  - ✅ **Synthetic Logic**: Automatic industry-standard fallback if no web data is found
  - ✅ **Permanent Memory**: Dynamic profile saving to `discoveries.json`
- ✅ Company-specific simulations (Google, Amazon, etc.)
- ✅ Adaptive difficulty levels (Junior, Mid-level, Senior)
- ✅ Panel interview mode with multiple AI personas
- ✅ Context-aware questioning based on resume and JD

### 📄 **Resume Analysis** (Backend Ready)
- ✅ ATS Score calculation (0-100)
- ✅ Gap analysis vs job descriptions
- ✅ Strengths & weaknesses identification
- ✅ Actionable improvement tips
- ⚠️ UI display pending

### 📊 **Evaluation System**
- ✅ No sugarcoating - Direct, professional feedback
- ✅ Behavioral vibe analysis (confidence, hesitation, assertiveness)
- ✅ Multi-dimensional scoring
- ✅ Comprehensive feedback after 5+ questions

### 🔐 Secure Authentication
- ✅ **Google OAuth 2.0**: Direct, secure login (No random or false email accounts)
- ✅ Protected API endpoints and persistent user sessions
- ✅ JWT-based verification for every request

### 🎨 **Premium UI/UX**
- ✅ Glassmorphism effects with advanced blur
- ✅ Animated mesh gradients
- ✅ 3D card transforms with magnetic hover
- ✅ Shimmering borders and gradient animations
- ✅ Professional meeting interface (Zoom/Meet inspired)
- ✅ Compact 64px toolbar
- ✅ Shimmer effects on primary buttons

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL 14+**
- **Gemini API Key** ([Get one here](https://aistudio.google.com/app/apikey))

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/interview-prep.git
cd interview-prep
```

#### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
echo "DATABASE_URL=postgresql://neondb_owner:[pass]@[endpoint].neon.tech/neondb?sslmode=require" >> .env

# Run database migrations (Syncs with Neon Cloud)
alembic upgrade head

# Start the backend server
python main.py
```

Backend will run on `http://127.0.0.1:8000`

#### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on `http://localhost:5173`

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Alembic** - Database migration tool
- **PostgreSQL** - Robust relational database
- **PyPDF** - PDF text extraction
- **Google Gemini 2.0 Flash** - Advanced AI model

### Frontend
- **React 18.3** - UI library
- **Vite** - Next-generation frontend tooling
- **Axios** - HTTP client
- **Vanilla CSS** - Custom styling with glassmorphism
- **Web Speech API** - Voice recognition

### Planned Infrastructure
- **GitHub** - Source control & CI/CD
- **Vercel** - Frontend deployment
- **Neon** - Serverless PostgreSQL Database (Cloud)
- **UPI QR Code** - Direct payment (Zero fees)
- **Let's Encrypt** - SSL certificates (Free)

---

## 📁 Project Structure

```
interview-prep/
├── backend/
│   ├── alembic/              # Database migrations
│   ├── services/
│   │   ├── gemini_service.py # AI service layer
│   │   └── company_intelligence.py # Company intelligence service (NEW)
│   ├── data/
│   │   └── company_profiles.json # Curated company database (NEW)
│   ├── models.py             # SQLAlchemy models
│   ├── schemas.py            # Pydantic schemas
│   ├── database.py           # Database configuration
│   ├── round_config.py       # Multi-round configuration
│   ├── main.py               # FastAPI application
│   ├── test_company_intel.py # Company intelligence test script (NEW)
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx # Main dashboard component
│   │   │   ├── LandingPage.jsx # Landing page
│   │   │   └── Login.jsx     # Login/Signup
│   │   ├── App.css           # Setup screen styles
│   │   ├── Meeting.css       # Interview screen styles
│   │   └── InterviewerCards.css # Card component styles
│   ├── index.html            # HTML entry point
│   └── package.json          # Node dependencies
└── README.md                 # This file
```

---

## 🔌 API Documentation

### Base URL
```
http://127.0.0.1:8000
```

### Endpoints

#### `GET /health`
Health check endpoint

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.1"
}
```

#### `POST /interviews/start`
Start a new interview session

**Request Body:**
```json
{
  "role_category": "Engineering & Tech",
  "sub_role": "Full Stack Developer",
  "difficulty_level": 1,
  "target_company": "Google",
  "is_panel": false,
  "interviewer_name": "Adinath"
}
```

**Response:**
```json
{
  "id": 1,
  "first_question": "Good evening! I am Adinath, simulating a Technical interview..."
}
```

#### `POST /interviews/upload-resume`
Start interview with resume analysis

**Form Data:**
- `file`: PDF file
- `role_category`: string
- `sub_role`: string
- `difficulty_level`: integer (1-3)
- `target_company`: string (optional)
- `interviewer_name`: string

**Response:**
```json
{
  "id": 1,
  "first_question": "...",
  "resume_analysis": {
    "ats_score": 85,
    "strengths": ["Strong technical background", "..."],
    "weaknesses": ["Missing cloud certifications", "..."],
    "tips": ["Add more quantifiable achievements", "..."]
  }
}
```

#### `POST /interviews/submit-answer`
Submit an answer and get next question or evaluation

**Request Body:**
```json
{
  "interview_id": 1,
  "answer": "I have 3 years of experience in full-stack development..."
}
```

**Response (Questions 1-4):**
```json
{
  "evaluation": null,
  "next_question": "That's interesting. Can you elaborate on...",
  "terminated": false,
  "questions_asked": 2
}
```

**Response (After 5+ questions):**
```json
{
  "evaluation": {
    "score": 7.5,
    "feedback": "Strong technical knowledge but needs more confidence...",
    "vibe_analysis": {
      "confidence_score": 7,
      "hesitation_level": "Medium",
      "assertiveness": "Could be more decisive in answers"
    },
    "can_proceed": true
  },
  "next_question": null,
  "terminated": true,
  "questions_asked": 5
}
```

---

## 🎯 Usage Guide

### Starting an Interview

1. **Navigate to the setup screen**
2. **Choose your interviewer** (Adinath or Veda)
3. **Select your role category** (12 categories available)
4. **Pick a sub-role** (specific to your category)
5. **Set difficulty level** (1=Junior, 2=Mid, 3=Senior)
6. **Optional**: Upload resume (PDF) for personalized questions
7. **Optional**: Add target company and job description
8. **Optional**: Enable panel mode for multi-interviewer experience
9. **Click "ENTER MEETING ROOM"**

### During the Interview

- **Microphone**: Auto-enabled for voice input
- **Camera**: Disabled by default - AI will ask you to enable it
- **Voice Recognition**: Speak naturally, AI transcribes in real-time
- **Submit Response**: Click when you've finished your answer
- **Leave**: Exit the interview at any time

### After the Interview (5+ questions)

- View your **comprehensive evaluation**
- See your **score out of 10**
- Read **detailed feedback** on your performance
- Get **behavioral analysis** of your communication style
- Review the **complete transcript** (future feature)

---

## 🔐 Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Required (ONLY PAID SERVICE)
GEMINI_API_KEY=your_gemini_api_key_here

# Database - Development (Local PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/interviewai

# Database - Production (Supabase - will switch during deployment)
# DATABASE_URL=postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres

# Optional (for future features)
SECRET_KEY=your_secret_key_for_jwt
DEBUG=True

# UPI Payment (FREE - Your UPI ID)
UPI_ID=yourname@paytm
UPI_NAME=Your Name
```

**Note**: Currently using local PostgreSQL (pgAdmin4). Will migrate to Supabase during deployment phase.

### 💰 Cost Breakdown

#### Development Phase (Current)
- **Gemini API**: ~₹0.10 per interview
- **Backend**: ₹0 (Local development)
- **Database**: ₹0 (PostgreSQL via pgAdmin4)
- **Frontend**: ₹0 (Local development)
- **Total**: ~₹50-100/month for Gemini API

#### Production Phase (After Deployment)
- **Gemini API**: ~₹0.10 per interview (~₹100-500/month)
- **AWS EC2**: ₹0 (Free tier 12 months), then ~₹500/month (t2.micro)
- **Supabase DB**: ₹0 (Free tier - 500MB, 2GB bandwidth)
- **Vercel**: ₹0 (Free tier)
- **SSL Certificates**: ₹0 (Let's Encrypt)
- **GitHub**: ₹0 (Free for public repos)
- **Payment Processing**: ₹0 (Direct UPI)
- **Total Year 1**: ~₹100-500/month (Gemini only)
- **Total Year 2+**: ~₹600-1000/month (Gemini + AWS)

#### Revenue Model (After Payment Integration)
- **Free Tier**: ₹0 (1 interview/2 weeks)
- **Pro Tier**: ₹199/month (Unlimited interviews)
- **Elite Tier**: ₹499/month (All features)
- **Break-even**: ~3-5 Pro users or 2 Elite users per month

---

## � Current Limitations & Known Issues

### Limitations
- ⚠️ Single round only (Technical/Screening)
- ⚠️ No interview history tracking
- ⚠️ Resume analysis not displayed in UI
- ⚠️ No deployment (local only)
- ⚠️ No payment integration
- ⚠️ No learning roadmap generation

### Known Issues
- None currently reported ✅

---

## 📚 Project Documentation

Explore the deeper technical reasoning and project history:
- [📜 Activity Log & Collaborators](./COLLABORATORS.md) - Track all major implementations and fixes.
- [🧠 Technical Challenges & Solutions](./CHALLENGES.md) - Deep dive into how we solved complex Agentic problems.
- [🗺️ Future Roadmap](./NEXT_STEPS.md) - See where the platform is headed next.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Gemini Team** for the powerful AI model
- **FastAPI** for the excellent web framework
- **React Team** for the robust UI library
- Inspired by industry-leading platforms like Zoom, Google Meet, and Linear

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

<div align="center">

**Built with ❤️ for those who want to be more than just 'prepared'**

### 🚀 Journey Status: Phase 1 Complete - Massive Challenges Ahead!

*We've cleared the first hurdle. More logic, more code, more challenges await.* 💪

⭐ Star this repo if you found it helpful!

</div>