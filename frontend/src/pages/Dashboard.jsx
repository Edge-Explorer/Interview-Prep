import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../App.css';
import '../Meeting.css';
import '../InterviewerCards.css';

const API_BASE = "http://127.0.0.1:8000";

function Dashboard() {
    const navigate = useNavigate();
    const [step, setStep] = useState('setup'); // setup, meeting, result
    const [loading, setLoading] = useState(false);
    const [preparingStep, setPreparingStep] = useState(0);

    const [interviewId, setInterviewId] = useState(null);
    const [messages, setMessages] = useState([]);
    const [userInput, setUserInput] = useState("");
    const [sessionData, setSessionData] = useState({
        role_category: "",
        sub_role: "",
        difficulty_level: 1,
        target_company: "",
        job_description: "",
        is_panel: false,
        interviewer_name: "Adinath"
    });
    const [resumeFile, setResumeFile] = useState(null);
    const [evaluation, setEvaluation] = useState(null);
    const [isListening, setIsListening] = useState(false);
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [isMicOn, setIsMicOn] = useState(true);
    const [isCamOn, setIsCamOn] = useState(false);
    const [stream, setStream] = useState(null);
    const videoRef = useRef(null);
    const recognitionRef = useRef(null);

    // Multi-round tracking
    const [currentRound, setCurrentRound] = useState("Technical");
    const [currentRoundNumber, setCurrentRoundNumber] = useState(1);
    const [roundsCompleted, setRoundsCompleted] = useState([]);
    const [roundScores, setRoundScores] = useState({});
    const [questionCount, setQuestionCount] = useState(0);
    const [showTransition, setShowTransition] = useState(false);
    const [transitionData, setTransitionData] = useState({ prevRound: "", nextRound: "", score: 0 });
    const [showPricing, setShowPricing] = useState(false);
    const [stats, setStats] = useState({ total_interviews: 0, avg_score: 0.0 });



    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const token = localStorage.getItem('token');

    useEffect(() => {
        if (!token) {
            navigate('/login');
        } else if (step === 'setup') {
            // Fetch real user stats
            const fetchStats = async () => {
                try {
                    const res = await axios.get(`${API_BASE}/users/stats`, {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    setStats(res.data);
                } catch (err) {
                    console.error("Error fetching stats:", err);
                }
            };
            fetchStats();
        }
    }, [token, navigate, step]);

    // Initialize Speech Recognition once
    useEffect(() => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            const recognition = new SpeechRecognition();
            recognition.lang = 'en-US';
            recognition.interimResults = true;
            recognition.continuous = true;

            recognition.onstart = () => setIsListening(true);
            recognition.onend = () => {
                if (step === 'meeting' && isMicOn) recognition.start(); // Auto-restart in meeting
            };

            recognition.onresult = (event) => {
                const transcript = Array.from(event.results)
                    .map(result => result[0])
                    .map(result => result.transcript)
                    .join('');
                setUserInput(transcript);
            };
            recognitionRef.current = recognition;
        }
    }, [step, isMicOn]);

    const toggleMic = () => {
        if (isMicOn) {
            recognitionRef.current?.stop();
        } else {
            recognitionRef.current?.start();
        }
        setIsMicOn(!isMicOn);
    };

    const toggleCam = async () => {
        if (!isCamOn) {
            try {
                const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
                setStream(mediaStream);
                if (videoRef.current) videoRef.current.srcObject = mediaStream;
                setIsCamOn(true);
            } catch (err) {
                console.error("Camera access denied", err);
            }
        } else {
            if (stream) {
                stream.getVideoTracks().forEach(track => {
                    track.stop();
                });
                if (videoRef.current) videoRef.current.srcObject = null;
            }
            setIsCamOn(false);
        }
    };

    const speak = (text) => {
        if (!text) return;
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.onstart = () => setIsSpeaking(true);
        utterance.onend = () => setIsSpeaking(false);
        const allVoices = window.speechSynthesis.getVoices();
        const interviewerIsVeda = sessionData.interviewer_name === "Veda";
        let selectedVoice = null;
        if (interviewerIsVeda) {
            selectedVoice = allVoices.find(v => {
                const n = v.name.toLowerCase();
                return n.includes('female') || n.includes('samantha') || n.includes('zira') || n.includes('vicki') || n.includes('google uk english female');
            });
            if (!selectedVoice && allVoices.length > 1) selectedVoice = allVoices[1];
        } else {
            selectedVoice = allVoices.find(v => {
                const n = v.name.toLowerCase();
                return n.includes('male') || n.includes('david') || n.includes('mark') || n.includes('google uk english male');
            });
            if (!selectedVoice) selectedVoice = allVoices[0];
        }
        utterance.voice = selectedVoice || allVoices[0];
        utterance.rate = 1.0;
        utterance.pitch = interviewerIsVeda ? 1.1 : 0.9;
        window.speechSynthesis.speak(utterance);
    };

    useEffect(() => {
        if (step === 'meeting') {
            if (isMicOn) recognitionRef.current?.start();
        }
        return () => {
            stream?.getTracks().forEach(t => t.stop());
        };
    }, [step, stream]);

    useEffect(() => {
        if (step === 'meeting' && messages.length > 0 && messages[messages.length - 1].role === 'assistant') {
            speak(messages[messages.length - 1].content);
        }
    }, [messages, step]);

    const startInterview = async () => {
        if (!resumeFile) {
            alert("Please upload your resume (PDF) to start a contextual AI interview. This helps our AI tailor questions specifically to your background!");
            return;
        }

        setLoading(true);
        setStep('preparing');
        setPreparingStep(1);

        // Step 1: Parsing Resume (if exists) or Just initializing
        const interval = setInterval(() => {
            setPreparingStep(prev => prev < 4 ? prev + 1 : prev);
        }, 2000);

        try {
            let res;
            if (resumeFile) {
                const formData = new FormData();
                formData.append('file', resumeFile);
                formData.append('role_category', sessionData.role_category);
                formData.append('sub_role', sessionData.sub_role);
                formData.append('difficulty_level', sessionData.difficulty_level);
                formData.append('target_company', sessionData.target_company);
                formData.append('is_panel', sessionData.is_panel);
                formData.append('job_description', sessionData.job_description);
                formData.append('interviewer_name', sessionData.interviewer_name);
                res = await axios.post(`${API_BASE}/interviews/upload-resume`, formData, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
            } else {
                res = await axios.post(`${API_BASE}/interviews/start`, {
                    ...sessionData,
                    difficulty_level: parseInt(sessionData.difficulty_level)
                }, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
            }
            setInterviewId(res.data.id);
            setMessages([{ role: 'assistant', content: res.data.first_question }]);
            setQuestionCount(1);

            clearInterval(interval);
            setPreparingStep(4);
            setTimeout(() => {
                setStep('meeting');
                setLoading(false);
            }, 1000);
        } catch (err) {
            clearInterval(interval);
            alert(`Error: ${err.message}`);
            setStep('setup');
            setLoading(false);
        }
    };

    const submitAnswer = async () => {
        if (!userInput.trim()) return;
        const currentInput = userInput;
        setUserInput("");
        setMessages(prev => [...prev, { role: 'user', content: currentInput }]);
        setLoading(true);
        window.speechSynthesis.cancel();

        try {
            const res = await axios.post(`${API_BASE}/interviews/submit-answer`, {
                interview_id: interviewId,
                answer: currentInput
            }, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (res.data.current_round) {
                setCurrentRound(res.data.current_round);
                setCurrentRoundNumber(res.data.current_round_number);
                setQuestionCount(res.data.questions_asked || 0);
            }

            if (res.data.round_completed) {
                setRoundsCompleted(res.data.rounds_completed || []);
                setRoundScores(res.data.round_scores || {});
                if (res.data.round_passed) {
                    if (res.data.interview_completed) {
                        setEvaluation(res.data.evaluation);
                        setStep('result');
                    } else {
                        const lastRound = res.data.rounds_completed[res.data.rounds_completed.length - 1];
                        setTransitionData({
                            prevRound: lastRound,
                            nextRound: res.data.next_round,
                            score: res.data.round_scores[lastRound]
                        });
                        setShowTransition(true);
                        setTimeout(() => {
                            setShowTransition(false);
                            setCurrentRound(res.data.next_round);
                            setCurrentRoundNumber(res.data.next_round_number);
                            setMessages(prev => [...prev, { role: 'assistant', content: res.data.next_question }]);
                            setQuestionCount(1);
                        }, 4000);
                    }
                } else {
                    setEvaluation(res.data.evaluation);
                    setStep('result');
                }
            } else {
                setEvaluation(res.data.evaluation);
                if (res.data.terminated) {
                    setStep('result');
                } else {
                    setMessages(prev => [...prev, { role: 'assistant', content: res.data.next_question }]);
                    setQuestionCount(res.data.questions_asked + 1);
                }
            }
        } catch (err) {
            alert("Submission failed.");
        }
        setLoading(false);
    };

    if (step === 'setup') {
        const roleCategories = ["Engineering & Tech", "Healthcare & Medical", "Business & Management", "Finance & Accounting", "Creative & Design", "Sales & Marketing", "Education & Training", "Legal", "Construction & Trades", "Hospitality & Tourism", "Social Services", "Science & Research"];
        const interviewers = [
            { name: "Adinath", gender: "Male", v: "male", desc: "Senior Mentor. Focuses on your technical fundamentals and core logic." },
            { name: "Veda", gender: "Female", v: "female", desc: "HR Specialist. Tests your communication skills and behavioral readiness." }
        ];

        return (
            <div className="dashboard-layout">
                <nav className="top-nav">
                    <div className="nav-left">
                        <div className="nav-logo">InterviewAI</div>
                        <div className="nav-tag">BETA</div>
                    </div>
                    <div className="nav-right">
                        <div className="user-profile-badge" onClick={() => setShowPricing(true)}>
                            <div className="user-avatar">
                                {user.full_name ? user.full_name.charAt(0).toUpperCase() : "G"}
                            </div>
                            <div className="user-details">
                                <span className="user-name">{user.full_name || "Guest User"}</span>
                                <span className="user-status">FREE PLAN</span>
                            </div>
                        </div>
                    </div>
                </nav>

                <main className="dashboard-content">
                    <header className="dashboard-header">
                        <div className="welcome-banner">
                            <h1>Welcome Back, {user.full_name?.split(' ')[0] || "Candidate"}! 👋</h1>
                            <p>Ready to ace your next big interview? Let's configure your practice session.</p>
                        </div>

                        <div className="quick-stats">
                            <div className="stat-card glass-card">
                                <span className="stat-label">AVG SCORE</span>
                                <span className="stat-value">⭐ {stats.avg_score}</span>
                            </div>
                            <div className="stat-card glass-card">
                                <span className="stat-label">INTERVIEWS</span>
                                <span className="stat-value">📊 {stats.total_interviews}</span>
                            </div>
                        </div>
                    </header>

                    <div className="glass-card setup-box">
                        <h2>Round Configuration</h2>
                        <div className="interviewer-selector" style={{ marginBottom: '25px' }}>
                            <label style={{ marginBottom: '10px', display: 'block' }}>Choose Your Interviewer</label>
                            <div className="interviewer-grid" style={{ display: 'flex', gap: '15px' }}>
                                {interviewers.map(int => (
                                    <div key={int.name} className={`interviewer-card glass-card ${sessionData.interviewer_name === int.name ? 'selected' : ''}`} onClick={() => setSessionData({ ...sessionData, interviewer_name: int.name })} style={{ flex: 1, padding: '15px', cursor: 'pointer', border: sessionData.interviewer_name === int.name ? '2px solid var(--primary)' : '1px solid var(--glass-border)', background: sessionData.interviewer_name === int.name ? 'rgba(99, 102, 241, 0.1)' : 'transparent' }}>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                                            <span style={{ fontSize: '1.2rem' }}>{int.gender === "Male" ? "👨‍💼" : "👩‍💼"}</span>
                                            <strong style={{ fontSize: '1.1rem' }}>{int.name}</strong>
                                        </div>
                                        <p style={{ fontSize: '0.8rem', opacity: 0.7, margin: 0 }}>{int.desc}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                        <div className="input-row">
                            <div className="input-group">
                                <label>Role Category</label>
                                <select value={sessionData.role_category} onChange={e => setSessionData({ ...sessionData, role_category: e.target.value })}>
                                    <option value="" disabled>Select Category</option>
                                    {roleCategories.map(r => <option key={r} value={r}>{r}</option>)}
                                </select>
                            </div>
                            <div className="input-group">
                                <label>Specific Sub-Role</label>
                                <input type="text" placeholder="e.g. Senior Backend Dev" value={sessionData.sub_role} onChange={e => setSessionData({ ...sessionData, sub_role: e.target.value })} />
                            </div>
                        </div>
                        <div className="input-row">
                            <div className="input-group">
                                <label>Target Company</label>
                                <input type="text" placeholder="e.g. Google" value={sessionData.target_company} onChange={e => setSessionData({ ...sessionData, target_company: e.target.value })} />
                            </div>
                            <div className="input-group">
                                <label>Difficulty</label>
                                <select value={sessionData.difficulty_level} onChange={e => setSessionData({ ...sessionData, difficulty_level: parseInt(e.target.value) })}>
                                    <option value={1}>Junior (Level 1)</option>
                                    <option value={2}>Mid (Level 2)</option>
                                    <option value={3}>Senior (Level 3)</option>
                                </select>
                            </div>
                        </div>
                        <div className="checkbox-group" style={{ margin: '10px 0' }}>
                            <input type="checkbox" id="panel" checked={sessionData.is_panel} onChange={e => setSessionData({ ...sessionData, is_panel: e.target.checked })} />
                            <label htmlFor="panel">Practice with a Panel (Mock Interview Mode)</label>
                        </div>
                        <div className="input-group">
                            <label>Upload Resume (PDF - Contextual AI Improvement) <span style={{ color: '#ef4444', fontSize: '0.7rem' }}>*REQUIRED</span></label>
                            <input type="file" accept=".pdf" onChange={e => setResumeFile(e.target.files[0])} />
                        </div>
                        <button className="primary-btn" onClick={startInterview} disabled={loading}>
                            {loading ? "PREPARING INTERVIEW..." : "START PRACTICE SESSION"}
                        </button>
                        <button className="secondary-btn" onClick={() => { localStorage.clear(); window.location.href = '/'; }} style={{ marginTop: '10px', background: 'transparent', border: '1px solid rgba(255,255,255,0.1)', color: 'rgba(255,255,255,0.5)', width: '100%', padding: '12px' }}>LOGOUT</button>
                    </div>

                    <footer className="disclaimer-footer">
                        <p>
                            <b>Disclaimer:</b> InterviewAI is an independent simulation platform. The AI personas, scenarios, and company-specific interview mocks are intended for practice purposes only. This platform and its AI interviewers (Adinath, Veda, etc.) are not affiliated with, endorsed by, or associated with any actual company, its employees, or its recruitment teams. Simulations are based on publicly available industry standards and do not guarantee actual interview outcomes.
                        </p>
                    </footer>
                </main>

                {showPricing && (
                    <div className="modal-overlay" onClick={() => setShowPricing(false)}>
                        <div className="pricing-modal glass-card" onClick={e => e.stopPropagation()}>
                            <button className="close-modal" onClick={() => setShowPricing(false)}>&times;</button>
                            <div className="pricing-header">
                                <h2>Upgrade Your Preparation</h2>
                                <p>Unlock premium AI personas, unlimited rounds, and advanced behavioral analytics.</p>
                            </div>
                            <div className="pricing-grid">
                                <div className="pricing-card glass-card">
                                    <div className="plan-badge">CURRENT</div>
                                    <h3>Basic</h3>
                                    <div className="price">₹0<span>/mo</span></div>
                                    <ul>
                                        <li>✅ 1 Interview/2 Weeks</li>
                                        <li>✅ Standard Technical Round</li>
                                        <li>✅ Basic AI Feedback</li>
                                        <li>❌ No Resume Analysis</li>
                                    </ul>
                                    <button className="plan-btn disabled">YOUR PLAN</button>
                                </div>
                                <div className="pricing-card glass-card pro">
                                    <div className="plan-badge featured">POPULAR</div>
                                    <h3>Pro</h3>
                                    <div className="price">₹199<span>/mo</span></div>
                                    <ul>
                                        <li>✅ Unlimited Interviews</li>
                                        <li>✅ All Technical Rounds</li>
                                        <li>✅ Resume-Tailored Questions</li>
                                        <li>✅ Star-Method Evaluation</li>
                                    </ul>
                                    <button className="plan-btn primary">UPGRADE NOW</button>
                                </div>
                                <div className="pricing-card glass-card elite">
                                    <h3>Elite</h3>
                                    <div className="price">₹499<span>/mo</span></div>
                                    <ul>
                                        <li>✅ Multi-Round Masterclass</li>
                                        <li>✅ 7-Day Custom Roadmap</li>
                                        <li>✅ Vibe & Speech Analytics</li>
                                        <li>✅ Panel Interview Mode</li>
                                    </ul>
                                    <button className="plan-btn secondary">GET ELITE</button>
                                </div>
                            </div>
                            <div className="payment-notice">
                                <p>✨ Zero Gateway Fees! Pay directly via UPI for instant activation.</p>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        );
    }

    if (step === 'preparing') {
        const analysisSteps = [
            { id: 1, text: resumeFile ? "Parsing your professional resume" : "Initializing platform context" },
            { id: 2, text: "Analyzing your experience & background" },
            { id: 3, text: "Extracting core skills & focus areas" },
            { id: 4, text: "Generating contextual interview questions" }
        ];

        return (
            <div className="preparing-container">
                <div className="analysis-card glass-card">
                    <div className="analysis-left">
                        <div className="analysis-icon-container">
                            {preparingStep === 4 ? "✨" : "🔍"}
                        </div>
                        <h2>{preparingStep === 4 ? "Ready!" : "Analyzing..."}</h2>
                        <p>Our AI is tailoring questions based on your specific projects and skills.</p>
                    </div>
                    <div className="analysis-right">
                        {analysisSteps.map(s => (
                            <div key={s.id} className={`analysis-step ${preparingStep >= s.id ? 'active' : ''} ${preparingStep > s.id ? 'completed' : ''}`}>
                                <div className="step-check">
                                    {preparingStep > s.id ? "✓" : s.id}
                                </div>
                                <span className="step-text">{s.text}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        );
    }


    if (step === 'meeting') {
        return (
            <div className="meeting-container">
                <div className="status-overlay">
                    <div className="live-dot"></div>
                    <span>LIVE INTERVIEW: {sessionData.target_company || "General Technical"} Round</span>
                </div>
                <div className="meeting-main">
                    <div className="interviewer-view glass-card">
                        <div className="avatar-container">
                            <div className="eye-pair">
                                <div className="eye"><div className="pupil" style={{ transform: isListening ? `translate(${(Math.random() - 0.5) * 10}px, ${(Math.random() - 0.5) * 10}px)` : 'translate(-50%, -50%)' }}></div></div>
                                <div className="eye"><div className="pupil" style={{ transform: isListening ? `translate(${(Math.random() - 0.5) * 10}px, ${(Math.random() - 0.5) * 10}px)` : 'translate(-50%, -50%)' }}></div></div>
                            </div>
                            <div className={`mouth ${isSpeaking ? 'speaking' : ''}`}></div>
                            <p style={{ marginTop: '20px', color: 'rgba(255,255,255,0.6)', maxWidth: '80%', textAlign: 'center' }}>{messages[messages.length - 1].content}</p>
                        </div>
                        <div className="candidate-view">
                            <video ref={videoRef} autoPlay playsInline muted />
                            {!isCamOn && <div className="cam-off-overlay">Camera Off</div>}
                        </div>
                    </div>
                </div>
                <div className="meeting-toolbar">
                    <button className={`tool-btn ${!isMicOn ? 'off' : ''}`} onClick={toggleMic}>{isMicOn ? '🎤' : '🎙️'}</button>
                    <button className={`tool-btn ${!isCamOn ? 'off' : ''}`} onClick={toggleCam}>{isCamOn ? '📹' : '📸'}</button>
                    <div className="tool-spacer"></div>
                    <div className="voice-input-preview">{userInput || "AI is listening to your answer..."}</div>
                    <div className="round-progress" style={{ color: 'rgba(255,255,255,0.6)', fontSize: '0.8rem', fontWeight: 'bold', margin: '0 10px' }}>Q: {questionCount}/5</div>
                    <button className="tool-btn primary" onClick={submitAnswer} disabled={loading}>{loading ? "EVALUATING..." : "SUBMIT RESPONSE"}</button>
                    <button className="tool-btn off end-btn" onClick={() => { window.speechSynthesis.cancel(); window.location.reload(); }}>LEAVE</button>
                </div>
                {showTransition && (
                    <div className="round-transition-overlay">
                        <div className="transition-content">
                            <div className="round-badge">ROUND {currentRoundNumber + 1} STARTING</div>
                            <h2>Great job in the {transitionData.prevRound} round!</h2>
                            <div className="next-round-name">{transitionData.nextRound}</div>
                            <div className="loader-bar-container"><div className="loader-bar"></div></div>
                            <p className="transition-disclaimer"><b>Disclaimer:</b> Final candidate evaluation, detailed feedback, and ATS resume analysis will be generated <b>after all rounds</b> are successfully completed.</p>
                        </div>
                    </div>
                )}
            </div>
        );
    }

    if (step === 'result') {
        return (
            <div className="result-container">
                <div className="glass-card result-box">
                    <h1 className={evaluation?.can_proceed ? "success-text" : "fail-text"}>{evaluation?.can_proceed ? "ROUND COMPLETE" : "INTERVIEW TERMINATED"}</h1>
                    <div className="score-circle"><span className="score-num">{evaluation?.score}</span><span className="total">/10</span></div>
                    <div className="feedback-section"><h3>Honest Recruiter Feedback:</h3><p>{evaluation?.feedback}</p></div>
                    <button className="secondary-btn" onClick={() => setStep('setup')}>BACK TO DASHBOARD</button>
                </div>
            </div>
        );
    }
}

export default Dashboard;
