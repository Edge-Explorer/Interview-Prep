# 🎯 InterviewAI - Premium AI Interview Simulation Platform

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![React](https://img.shields.io/badge/react-18.3+-61DAFB.svg)
![Gemini](https://img.shields.io/badge/Gemini-2.0%20Flash-orange.svg)

**The Ultimate AI-Powered Interview Preparation Platform**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Tech Stack](#-tech-stack) • [API Docs](#-api-documentation)

</div>

---

## 🌟 Overview

InterviewAI is a **state-of-the-art interview simulation platform** powered by **Google's Gemini 2.0 Flash**. It provides realistic, industry-level interview experiences with AI personas that simulate real technical interviewers from top companies like Google, Amazon, Microsoft, and more.

### 🎭 Meet Your AI Interviewers

- **Adinath** - *The Primal Sage*: Strict, direct, and explores the depth of your foundations
- **Veda** - *The Eternal Wisdom*: Insightful, observant, and tests your clarity and vision

---

## ✨ Premium Features

### 🎤 **Live Interview Simulation**
- **Real-time voice recognition** for natural conversation flow
- **Dynamic AI responses** that adapt to your answers
- **Industry-standard UI** with professional glassmorphism design
- **Live video feed** with camera controls for authenticity
- **Minimum 5 questions** before evaluation for comprehensive assessment

### 🧠 **Intelligent Interview System**
- **Multi-persona AI interviewers** with distinct personalities
- **Company-specific simulations** (Google, Amazon, Microsoft, etc.)
- **Adaptive difficulty levels** (Junior, Mid-level, Senior/Lead)
- **Panel interview mode** with multiple AI interviewers
- **Context-aware questioning** based on your resume and job description

### 📄 **Premium Resume Analysis**
- **ATS Score calculation** (0-100)
- **Gap analysis** comparing your resume to job descriptions
- **Strengths & weaknesses identification**
- **Actionable improvement tips**
- **Privacy-first**: In-memory PDF processing, no storage

### 📊 **Honest Evaluation System**
- **No sugarcoating** - Direct, professional feedback
- **Behavioral vibe analysis** - Confidence, hesitation, assertiveness scoring
- **Multi-dimensional scoring** across technical accuracy and soft skills
- **Comprehensive feedback** after minimum 5 questions
- **Performance tracking** across multiple sessions

### 🎨 **Industry-Level UI/UX**
- **Premium glassmorphism design** matching top SaaS products
- **Animated mesh gradients** and particle effects
- **Sophisticated micro-interactions** and hover effects
- **Responsive design** for all screen sizes
- **Professional meeting interface** inspired by Zoom/Google Meet

### 🔒 **Security & Privacy**
- **Camera disabled by default** - User controls when to enable
- **No data storage** of video/audio streams
- **Secure API key management** via environment variables
- **Session-based authentication** ready for implementation

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
echo "DATABASE_URL=postgresql://user:password@localhost/interviewai" >> .env

# Run database migrations
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

## 🎯 Usage Guide

### Starting an Interview

1. **Navigate to the setup screen**
2. **Choose your interviewer** (Adinath or Veda)
3. **Select your role category** (Engineering & Tech, Healthcare, Business, etc.)
4. **Pick a sub-role** (Full Stack Developer, Data Scientist, etc.)
5. **Set difficulty level** (Junior, Mid-level, Senior)
6. **Optional**: Upload your resume (PDF) for personalized questions
7. **Optional**: Add target company and job description
8. **Click "ENTER MEETING ROOM"**

### During the Interview

- **Microphone**: Auto-enabled for voice input
- **Camera**: Disabled by default - enable when AI requests for authenticity
- **Voice Recognition**: Speak naturally, AI transcribes in real-time
- **Submit Response**: Click when you've finished your answer
- **Leave**: Exit the interview at any time

### After the Interview

- View your **comprehensive evaluation**
- See your **score out of 10**
- Read **detailed feedback** on your performance
- Get **behavioral analysis** of your communication style
- Review the **complete transcript**

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

### AI & ML
- **Gemini 2.0 Flash** - Multi-modal AI model
- **Context-aware prompting** - Dynamic system instructions
- **Structured JSON outputs** - Reliable evaluation format

---

## 📁 Project Structure

```
interview-prep/
├── backend/
│   ├── alembic/              # Database migrations
│   ├── services/
│   │   └── gemini_service.py # AI service layer
│   ├── models.py             # SQLAlchemy models
│   ├── schemas.py            # Pydantic schemas
│   ├── database.py           # Database configuration
│   ├── main.py               # FastAPI application
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main application component
│   │   ├── App.css           # Setup screen styles
│   │   ├── Meeting.css       # Interview screen styles
│   │   └── InterviewerCards.css # Card component styles
│   ├── index.html            # HTML entry point
│   └── package.json          # Node dependencies
└── README.md                 # This file
```

---

## � API Documentation

### Base URL
```
http://127.0.0.1:8000
```

### Endpoints

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
  "first_question": "Good evening! I am Adinath..."
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
    "strengths": [...],
    "weaknesses": [...],
    "tips": [...]
  }
}
```

#### `POST /interviews/submit-answer`
Submit an answer and get next question

**Request Body:**
```json
{
  "interview_id": 1,
  "answer": "I have 3 years of experience..."
}
```

**Response:**
```json
{
  "evaluation": null,
  "next_question": "That's interesting. Can you tell me...",
  "terminated": false,
  "questions_asked": 2
}
```

---

## 🎨 UI Features

### Premium Design Elements
- **Animated mesh gradients** for dynamic backgrounds
- **Glassmorphism effects** with advanced blur and saturation
- **Floating particle systems** for immersive experience
- **3D card transforms** with magnetic hover effects
- **Shimmering borders** and gradient animations
- **Professional typography** with custom font weights
- **Micro-interactions** on all interactive elements

### Meeting Interface
- **Compact toolbar** (64px height) for maximum screen space
- **Premium button hierarchy** with clear visual distinction
- **Shimmer effects** on primary actions
- **Professional camera controls** with blur overlay when off
- **Live status indicator** with pulsing animation
- **Voice preview** with real-time transcription display

---

## 🔐 Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/interviewai

# Optional
SECRET_KEY=your_secret_key_for_jwt
DEBUG=True
```

---

## 🚦 Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Building for Production

#### Backend
```bash
cd backend
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

#### Frontend
```bash
cd frontend
npm run build
```

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

⭐ Star this repo if you found it helpful!

</div>